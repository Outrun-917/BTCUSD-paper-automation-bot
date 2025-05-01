from data_feed import fetch_candles  # ✅ No get_okx_client needed anymore
from indicators import apply_indicators
from strategy import check_entry
from tv_trader import execute_trade
from utils import can_trade
from config import CONFIG
import time

def main():
    print("⏳ Starting bot... Open TradingView Paper Trading manually.")
    time.sleep(3)  # wait for user to open chart

    while True:
        try:
            df = fetch_candles(CONFIG["symbol"], CONFIG["timeframe"])
            if df is None:
                continue

            df = apply_indicators(df)
            signal = check_entry(df)

            if signal and can_trade(CONFIG["trade_cooldown"]):
                current_price = df.iloc[-1]["close"]
                print(f"[Signal] {signal.upper()} @ ${current_price:.2f}")
                execute_trade(
                    signal=signal,
                    current_price=current_price,
                    tp_pct=CONFIG["tp_pct"],
                    sl_pct=CONFIG["sl_pct"]
                )
            else:
                print("No trade: waiting for valid signal or cooldown.")

        except Exception as e:
            print(f"[ERROR] {e}")
        time.sleep(10)

if __name__ == "__main__":
    main()
