from data_feed import get_okx_client, fetch_candles
from indicators import apply_indicators
from strategy import check_entry
from tv_trader import execute_trade, open_browser
from utils import can_trade
from config import CONFIG
import time

def main():
    open_browser()
    print("Waiting for TradingView to load...")
    time.sleep(15)  # Give time for chart to open

    client = get_okx_client()

    while True:
        try:
            df = fetch_candles(client, CONFIG["symbol"], CONFIG["timeframe"])
            df = apply_indicators(df)
            signal = check_entry(df)

            if signal and can_trade(CONFIG["trade_cooldown"]):
                print(f"[Signal] {signal.upper()} at {df.iloc[-1]['close']}")
                execute_trade(signal)
            else:
                print("No signal or cooldown not met.")

        except Exception as e:
            print(f"[Error] {e}")
        time.sleep(10)

if __name__ == "__main__":
    main()
