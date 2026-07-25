import logging
import time

from config import CONFIG
from data_feed import fetch_candles
from indicators import apply_indicators
from strategy import check_entry
from tv_trader import execute_trade, close_position
from utils import can_trade, record_trade, seconds_until_next_candle

log = logging.getLogger(__name__)


class Position:
    def __init__(self, side, entry_price, tp_price, sl_price, atr_at_entry):
        self.side = side
        self.entry_price = entry_price
        self.tp_price = tp_price
        self.sl_price = sl_price
        self.atr_at_entry = atr_at_entry
        self.best_price = entry_price
        self.trailing_sl = sl_price

    def update(self, current_price):
        if self.side == "long":
            if current_price > self.best_price:
                self.best_price = current_price
                if self.best_price - self.entry_price >= CONFIG["trail_activate_atr"] * self.atr_at_entry:
                    new_trail = self.best_price - CONFIG["trail_sl_atr"] * self.atr_at_entry
                    if new_trail > self.trailing_sl:
                        log.info("Trailing SL updated: %.2f -> %.2f", self.trailing_sl, new_trail)
                        self.trailing_sl = new_trail
        else:
            if current_price < self.best_price:
                self.best_price = current_price
                if self.entry_price - self.best_price >= CONFIG["trail_activate_atr"] * self.atr_at_entry:
                    new_trail = self.best_price + CONFIG["trail_sl_atr"] * self.atr_at_entry
                    if new_trail < self.trailing_sl:
                        log.info("Trailing SL updated: %.2f -> %.2f", self.trailing_sl, new_trail)
                        self.trailing_sl = new_trail

    def check_exit(self, current_price):
        if self.side == "long":
            if current_price <= self.trailing_sl:
                return "sl"
            if current_price >= self.tp_price:
                return "tp"
        else:
            if current_price >= self.trailing_sl:
                return "sl"
            if current_price <= self.tp_price:
                return "tp"
        return None


def main():
    logging.basicConfig(
        level=CONFIG["log_level"],
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    position = None
    log.info("Bot started. Waiting for signal...")

    while True:
        try:
            df = fetch_candles(CONFIG["symbol"], CONFIG["timeframe"], limit=CONFIG["fetch_limit"])
            if df is None:
                log.warning("No data, retrying next candle")
                time.sleep(seconds_until_next_candle() + 1)
                continue

            df = apply_indicators(df, vwap_window=CONFIG["vwap_window"], atr_period=CONFIG["atr_period"],
                                  bb_period=CONFIG["bollinger_period"], bb_dev=CONFIG["bollinger_dev"])
            current_price = df["close"].iloc[-1]
            current_atr = df["atr"].iloc[-1]

            # --- No open position: check entry ---
            if position is None:
                signal = check_entry(df)
                if signal and can_trade(CONFIG["trade_cooldown"]):
                    if signal == "long":
                        tp_price = current_price + CONFIG["tp_atr_mult"] * current_atr
                        sl_price = current_price - CONFIG["sl_atr_mult"] * current_atr
                    else:
                        tp_price = current_price - CONFIG["tp_atr_mult"] * current_atr
                        sl_price = current_price + CONFIG["sl_atr_mult"] * current_atr

                    if execute_trade(signal, current_price, tp_price, sl_price):
                        position = Position(signal, current_price, tp_price, sl_price, current_atr)
                        record_trade()
                        log.info("Entered %s @ %.2f  TP %.2f  SL %.2f", signal.upper(), current_price, tp_price, sl_price)

            # --- Open position: update trailing stop + check exit ---
            else:
                position.update(current_price)
                exit_signal = position.check_exit(current_price)

                if exit_signal == "sl":
                    log.info("Trailing SL hit @ %.2f — closing position", current_price)
                    close_position()
                    position = None

                elif exit_signal == "tp":
                    log.info("TP hit @ %.2f — position closed by TV", current_price)
                    position = None

                else:
                    log.debug("Monitoring %s  price=%.2f  trail_sl=%.2f  tp=%.2f",
                              position.side.upper(), current_price, position.trailing_sl, position.tp_price)

        except Exception as e:
            log.error("Error in main loop: %s", e)

        time.sleep(seconds_until_next_candle() + 1)


if __name__ == "__main__":
    main()
