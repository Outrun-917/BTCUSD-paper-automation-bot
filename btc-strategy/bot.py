import logging
import time

from config import CONFIG
from data_feed import fetch_candles
from indicators import apply_indicators
from strategy import check_entry
from utils import can_trade, record_trade, seconds_until_next_candle

if not CONFIG["dry_run"]:
    from tv_trader import execute_trade, close_position

log = logging.getLogger(__name__)


class Position:
    def __init__(self, side, entry_price, tp_price, sl_price, atr_at_entry):
        self.side = side
        self.entry_price = entry_price
        self.tp_price = tp_price
        self.sl_price = sl_price
        self.atr_at_entry = atr_at_entry
        self.trailing_sl = sl_price

    def update(self, swing_low, swing_high):
        if self.side == "long":
            if swing_low > self.trailing_sl:
                log.info("Trailing SL updated: %.2f -> %.2f", self.trailing_sl, swing_low)
                self.trailing_sl = swing_low
        else:
            if swing_high < self.trailing_sl:
                log.info("Trailing SL updated: %.2f -> %.2f", self.trailing_sl, swing_high)
                self.trailing_sl = swing_high

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

    dry_run = CONFIG["dry_run"]
    mode = "DRY RUN" if dry_run else "LIVE"
    position = None
    wins = 0
    losses = 0

    log.info("Bot started (%s mode). Waiting for signal...", mode)

    while True:
        try:
            df = fetch_candles(CONFIG["symbol"], CONFIG["timeframe"], limit=CONFIG["fetch_limit"])
            if df is None:
                log.warning("No data, retrying next candle")
                time.sleep(seconds_until_next_candle() + 1)
                continue

            df = apply_indicators(df, vwap_window=CONFIG["vwap_window"], atr_period=CONFIG["atr_period"],
                                  bb_period=CONFIG["bollinger_period"], bb_dev=CONFIG["bollinger_dev"],
                                  volume_period=CONFIG["volume_period"])
            current_price = df["close"].iloc[-1]
            current_atr = df["atr"].iloc[-1]
            current_rsi = df["rsi"].iloc[-1]

            pos_info = f"{position.side.upper()} entry={position.entry_price:.2f}" if position else "none"
            log.info("Price %.2f  RSI %.1f  ATR %.2f  position=%s  W/L %d/%d  [%s]",
                     current_price, current_rsi, current_atr, pos_info, wins, losses, mode)

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

                    if dry_run:
                        position = Position(signal, current_price, tp_price, sl_price, current_atr)
                        record_trade()
                        log.info("Entered %s @ %.2f  TP %.2f  SL %.2f  [%s]",
                                 signal.upper(), current_price, tp_price, sl_price, mode)
                    elif execute_trade(signal, current_price, tp_price, sl_price):
                        position = Position(signal, current_price, tp_price, sl_price, current_atr)
                        record_trade()
                        log.info("Entered %s @ %.2f  TP %.2f  SL %.2f  [%s]",
                                 signal.upper(), current_price, tp_price, sl_price, mode)

            # --- Open position: update trailing stop + check exit ---
            else:
                lb = CONFIG["swing_lookback"]
                swing_low = df["low"].iloc[-lb:].min()
                swing_high = df["high"].iloc[-lb:].max()
                position.update(swing_low, swing_high)
                exit_signal = position.check_exit(current_price)

                if exit_signal == "sl":
                    if position.side == "long":
                        pnl = (current_price - position.entry_price) / position.entry_price * 100
                    else:
                        pnl = (position.entry_price - current_price) / position.entry_price * 100
                    if pnl > 0:
                        wins += 1
                    else:
                        losses += 1
                    log.info("SL hit @ %.2f  PnL %.2f%%  W/L %d/%d  [%s]",
                             current_price, pnl, wins, losses, mode)
                    if not dry_run:
                        close_position()
                    position = None

                elif exit_signal == "tp":
                    if position.side == "long":
                        pnl = (current_price - position.entry_price) / position.entry_price * 100
                    else:
                        pnl = (position.entry_price - current_price) / position.entry_price * 100
                    wins += 1
                    log.info("TP hit @ %.2f  PnL +%.2f%%  W/L %d/%d  [%s]",
                             current_price, pnl, wins, losses, mode)
                    if not dry_run:
                        close_position()
                    position = None

                else:
                    log.debug("Monitoring %s  price=%.2f  trail_sl=%.2f  tp=%.2f  [%s]",
                              position.side.upper(), current_price, position.trailing_sl,
                              position.tp_price, mode)

        except Exception as e:
            log.error("Error in main loop: %s", e)

        time.sleep(seconds_until_next_candle() + 1)


if __name__ == "__main__":
    main()
