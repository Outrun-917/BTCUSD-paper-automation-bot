# NQ1! Auto Scalper Bot (Visual Paper Trading via TradingView)

> **Disclaimer:** Experimental bot. Do not use with real money.

## Description

- Fetches NQ=F (Nasdaq 100 E-mini futures) 15m candles from Yahoo Finance via `yfinance`
- **Pure TJR price-action strategy**: Liquidity sweep + Break of Structure (BOS) — no RSI/BB/VWAP indicators
- Exit: Trailing stop only (swing-based, no fixed TP)
- Executes paper trades on TradingView via screen automation (pyautogui)

## Setup

```bash
pip install -r requirements.txt
```

## Calibration

Before running the bot, calibrate TradingView screen coordinates:

```bash
python calibrate_coords.py
```

This will guide you through hovering over each button in TradingView and capturing its position. Copy the output into `tv_trader.py` under `POSITIONS`.

## Running

```bash
python bot.py
```

By default runs in **dry-run mode** (simulates trades locally). Set `dry_run: False` in `config.py` to execute on TradingView via pyautogui.

## Backtesting

```bash
python backtest.py
```

Reports: trades, win rate, final equity, max drawdown, Sharpe ratio.

## Configuration

All parameters are in `config.py`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `dry_run` | True | Simulate trades locally (True) or execute on TradingView (False) |
| `symbol` | NQ=F | Yahoo Finance ticker for Nasdaq 100 E-mini futures |
| `timeframe` | 15m | Candle timeframe |
| `swing_structure_period` | 3 | Fractal N: swing high/low = highest/lowest in 2N+1 candle window |
| `swing_lookback_sweep` | 20 | Candles to scan for recent liquidity sweep |
| `bos_lookback` | 10 | Candles to scan for break of structure |
| `atr_period` | 14 | ATR period (for position sizing only) |
| `sl_atr_mult` | 1.5 | Initial stop-loss = entry +/- 1.5 * ATR (safety net) |
| `swing_lookback` | 3 | Trailing stop = lowest low / highest high of last N candles |
| `trade_start_hour` | 8 | Trade start hour ET (8 = pre-market) |
| `trade_end_hour` | 16 | Trade end hour ET (16 = market close) |
| `risk_pct` | 0.01 | 1% of balance risked per trade (backtest only) |
| `trade_cooldown` | 300 | Minimum seconds between trades |
| `fetch_limit` | 500 | Candles to fetch |

## TJR Strategy

This bot implements TJR's pure price-action methodology:

### Entry: Sweep + BOS

1. **Swing Structure** — Fractal-based swing highs and lows (N=3: highest/lowest in 7-candle window)
2. **Liquidity Sweep** — Price wicks beyond a swing level (grabs liquidity/stops), then closes back inside
3. **Break of Structure (BOS)** — Price closes beyond the opposing swing level, confirming reversal
4. **Entry** — Enter immediately after sweep + BOS align

### Exit: Trailing Stop Only

- Initial SL: 1.5x ATR from entry (safety net)
- Trailing stop: Ratchets to the lowest low (long) or highest high (short) of the last 3 candles
- No fixed TP — let winners run

### Backtesting Results (Revelio Trading)

TJR's own backtesting on NQ showed:
- Simple sweep + BOS (V1): **+20% average**
- Adding RSI/BB/VWAP confluence: **+4% average** (more confluence = worse)
- Trailing stops beat fixed TP

## Architecture

```
config.py       — All parameters
data_feed.py    — yfinance data fetcher
indicators.py   — ATR only (for position sizing)
strategy.py     — Pure TJR: swing detection, sweep, BOS
bot.py          — Live/dry-run loop with trailing stop management
backtest.py     — Backtester with trailing stop only
tv_trader.py    — TradingView pyautogui execution
utils.py        — Trade cooldown + candle timing helpers
calibrate_coords.py — TradingView coordinate calibrator
```

## Archived

The previous BTC/USD strategy is archived in `btc-strategy/` for reference.
