from data_feed import fetch_candles
from indicators import apply_indicators
from strategy import check_entry
from tv_trader import execute_trade
from utils import can_trade
from config import CONFIG
import time

position = None
entry_price = None

def main():
    global position, entry_price

    print("Bot started. Waiting for signal...")

    while True:
        try:
            df = fetch_candles(CONFIG["symbol"], CONFIG["timeframe"])
            if df is None:
                continue

            df = apply_indicators(df)
            signal = check_entry(df)
            current_price = df["close"].iloc[-1]

            # No open position
            if position is None and signal and can_trade(CONFIG["trade_cooldown"]):
                execute_trade(
                    signal=signal,
                    current_price=current_price,
                    tp_pct=CONFIG["tp_pct"],
                    sl_pct=CONFIG["sl_pct"]
                )
                entry_price = current_price
                position = signal
                print(f"[POSITION] Entered {position.upper()} at {entry_price:.2f}")

            # Monitor open position
            elif position == "long":
                tp = entry_price * (1 + CONFIG["tp_pct"])
                sl = entry_price * (1 - CONFIG["sl_pct"])
                if current_price >= tp:
                    print(f"[EXIT] TP hit. Closed LONG at {current_price:.2f}")
                    position = None
                elif current_price <= sl:
                    print(f"[EXIT] SL hit. Closed LONG at {current_price:.2f}")
                    position = None

            elif position == "short":
                tp = entry_price * (1 - CONFIG["tp_pct"])
                sl = entry_price * (1 + CONFIG["sl_pct"])
                if current_price <= tp:
                    print(f"[EXIT] TP hit. Closed SHORT at {current_price:.2f}")
                    position = None
                elif current_price >= sl:
                    print(f"[EXIT] SL hit. Closed SHORT at {current_price:.2f}")
                    position = None

            else:
                print("Monitoring...")

        except Exception as e:
            print(f"[ERROR] {e}")
        time.sleep(10)

if __name__ == "__main__":
    main()
