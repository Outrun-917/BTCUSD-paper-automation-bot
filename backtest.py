import logging
import math

import pandas as pd

from config import CONFIG
from data_feed import fetch_candles
from indicators import apply_indicators
from strategy import check_entry

log = logging.getLogger(__name__)

# --- Backtest Config ---
WARMUP = 200
START_BALANCE = 100_000
RISK_PCT = CONFIG["risk_pct"]
TP_MULT = CONFIG["tp_atr_mult"]
SL_MULT = CONFIG["sl_atr_mult"]
TRAIL_ACTIVATE = CONFIG["trail_activate_atr"]
TRAIL_SL_MULT = CONFIG["trail_sl_atr"]


def run_backtest(df):
    df = apply_indicators(df, vwap_window=CONFIG["vwap_window"], atr_period=CONFIG["atr_period"],
                          bb_period=CONFIG["bollinger_period"], bb_dev=CONFIG["bollinger_dev"])
    df.dropna(inplace=True)

    balance = START_BALANCE
    peak_balance = START_BALANCE
    position = None
    entry_price = None
    sl_price = None
    tp_price = None
    best_price = None
    trailing_sl = None
    atr_at_entry = None
    wins = 0
    losses = 0
    equity_curve = [START_BALANCE]
    daily_returns = []

    for i in range(WARMUP, len(df)):
        row = df.iloc[i]
        price = row["close"]
        atr = row["atr"]

        # --- No open position: check for entry ---
        if position is None:
            signal = check_entry(df.iloc[:i + 1])
            if signal:
                position = signal
                entry_price = price
                atr_at_entry = atr
                best_price = price

                if position == "long":
                    sl_price = entry_price - SL_MULT * atr_at_entry
                    tp_price = entry_price + TP_MULT * atr_at_entry
                    trailing_sl = sl_price
                else:
                    sl_price = entry_price + SL_MULT * atr_at_entry
                    tp_price = entry_price - TP_MULT * atr_at_entry
                    trailing_sl = sl_price
                continue

        # --- Open position: update trailing stop ---
        if position == "long":
            if price > best_price:
                best_price = price
                if best_price - entry_price >= TRAIL_ACTIVATE * atr_at_entry:
                    new_trail = best_price - TRAIL_SL_MULT * atr_at_entry
                    if new_trail > trailing_sl:
                        trailing_sl = new_trail

            # Check exit: SL first (worst case), then TP
            if row["low"] <= trailing_sl:
                exit_price = trailing_sl
                pnl_pct = (exit_price - entry_price) / entry_price
                balance += balance * RISK_PCT * pnl_pct / SL_MULT
                losses += 1
                log.info("LONG SL  @ %.2f  (pnl %.2f%%)", exit_price, pnl_pct * 100)
                position = None
            elif row["high"] >= tp_price:
                exit_price = tp_price
                pnl_pct = (exit_price - entry_price) / entry_price
                balance += balance * RISK_PCT * pnl_pct / SL_MULT
                wins += 1
                log.info("LONG TP  @ %.2f  (pnl %.2f%%)", exit_price, pnl_pct * 100)
                position = None

        elif position == "short":
            if price < best_price:
                best_price = price
                if entry_price - best_price >= TRAIL_ACTIVATE * atr_at_entry:
                    new_trail = best_price + TRAIL_SL_MULT * atr_at_entry
                    if new_trail < trailing_sl:
                        trailing_sl = new_trail

            if row["high"] >= trailing_sl:
                exit_price = trailing_sl
                pnl_pct = (entry_price - exit_price) / entry_price
                balance += balance * RISK_PCT * pnl_pct / SL_MULT
                losses += 1
                log.info("SHORT SL @ %.2f  (pnl %.2f%%)", exit_price, pnl_pct * 100)
                position = None
            elif row["low"] <= tp_price:
                exit_price = tp_price
                pnl_pct = (entry_price - exit_price) / entry_price
                balance += balance * RISK_PCT * pnl_pct / SL_MULT
                wins += 1
                log.info("SHORT TP @ %.2f  (pnl %.2f%%)", exit_price, pnl_pct * 100)
                position = None

        # Track equity curve
        equity_curve.append(balance)
        if len(equity_curve) > 1:
            daily_returns.append((equity_curve[-1] - equity_curve[-2]) / equity_curve[-2])

        peak_balance = max(peak_balance, balance)

    # --- Report ---
    total = wins + losses
    winrate = (wins / total) * 100 if total else 0

    # Max drawdown
    max_dd = 0.0
    peak = equity_curve[0]
    for eq in equity_curve:
        peak = max(peak, eq)
        dd = (peak - eq) / peak
        max_dd = max(max_dd, dd)

    # Sharpe ratio (annualized, assuming 1m candles)
    sharpe = 0.0
    if daily_returns and len(daily_returns) > 1:
        avg_ret = sum(daily_returns) / len(daily_returns)
        std_ret = (sum((r - avg_ret) ** 2 for r in daily_returns) / len(daily_returns)) ** 0.5
        if std_ret > 0:
            sharpe = (avg_ret / std_ret) * math.sqrt(525_600)  # annualize from 1m bars

    print("\n--- BACKTEST REPORT ---")
    print(f"Trades       : {total}")
    print(f"Wins         : {wins}")
    print(f"Losses       : {losses}")
    print(f"Win Rate     : {winrate:.2f}%")
    print(f"Final Equity : ${balance:,.2f}")
    print(f"Max Drawdown : {max_dd:.2%}")
    print(f"Sharpe Ratio : {sharpe:.2f}")

    return {
        "trades": total,
        "wins": wins,
        "losses": losses,
        "winrate": winrate,
        "final_equity": balance,
        "max_drawdown": max_dd,
        "sharpe": sharpe,
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    df = fetch_candles(symbol=CONFIG["symbol"], timeframe=CONFIG["timeframe"], limit=CONFIG["fetch_limit"])
    if df is not None:
        run_backtest(df)
    else:
        print("Failed to fetch data.")
