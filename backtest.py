import pandas as pd
from data_feed import fetch_data_yahoo
from indicators import apply_indicators
from strategy import check_entry
from ta.volatility import AverageTrueRange

# --- Config ---
WARMUP = 200
START_BALANCE = 100_000
RISK_PCT = 0.01
TP_MULTIPLIER = 2.5
SL_MULTIPLIER = 1.5

# --- Backtest Engine ---
def run_backtest(df):
    df = apply_indicators(df)
    df.dropna(inplace=True)
    df["atr"] = AverageTrueRange(high=df["high"], low=df["low"], close=df["close"]).average_true_range()

    balance = START_BALANCE
    position = None
    entry_price = None
    wins = 0
    losses = 0

    for i in range(WARMUP, len(df)):
        row = df.iloc[i]
        price = row["close"]
        atr = row["atr"]

        if not position:
            signal = check_entry(df.iloc[:i+1])
            if signal:
                position = signal
                entry_price = price
                risk_amt = balance * RISK_PCT

                if position == "long":
                    sl = entry_price - SL_MULTIPLIER * atr
                    tp = entry_price + TP_MULTIPLIER * atr
                else:
                    sl = entry_price + SL_MULTIPLIER * atr
                    tp = entry_price - TP_MULTIPLIER * atr
                continue

        if position == "long":
            if row["low"] <= sl:
                balance -= balance * RISK_PCT
                losses += 1
                position = None
            elif row["high"] >= tp:
                balance += balance * RISK_PCT
                wins += 1
                position = None

        elif position == "short":
            if row["high"] >= sl:
                balance -= balance * RISK_PCT
                losses += 1
                position = None
            elif row["low"] <= tp:
                balance += balance * RISK_PCT
                wins += 1
                position = None

    total = wins + losses
    winrate = (wins / total) * 100 if total else 0
    print("\n--- BACKTEST REPORT ---")
    print(f"Trades      : {total}")
    print(f"Wins        : {wins}")
    print(f"Losses      : {losses}")
    print(f"Win Rate    : {winrate:.2f}%")
    print(f"Final Equity: ${balance:,.2f}")

if __name__ == "__main__":
    df = fetch_data_yahoo(symbol="BTC-USD", interval="1m", period="7d", cache_file="btc_1m.csv")
    run_backtest(df)