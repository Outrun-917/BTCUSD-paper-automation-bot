# BTCUSD Auto Scalper Bot (Visual Paper Trading via TradingView)

> **Disclaimer:** Experimental bot. Do not use with real money.

## Description

- Fetches BTC/USD 5m candles from OKX via `ccxt` (paginated)
- Technical indicators: RSI, Bollinger Bands, Rolling VWAP (24h), ATR, volume average
- Entry signals: RSI extreme + BB band break + VWAP confluence + candle confirmation + VWAP slope filter
- Exit: ATR-based TP/SL with swing-based trailing stop
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

## Backtesting

```bash
python backtest.py
```

Reports: trades, win rate, final equity, max drawdown, Sharpe ratio.

## Configuration

All parameters are in `config.py`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `rsi_period` | 14 | RSI lookback |
| `bollinger_period` | 20 | Bollinger Bands period |
| `bollinger_dev` | 2 | Bollinger Bands std dev |
| `vwap_window` | 288 | Rolling VWAP window (288 = 24h of 5m candles) |
| `atr_period` | 14 | ATR period |
| `rsi_oversold` | 32 | Long entry threshold |
| `rsi_overbought` | 68 | Short entry threshold |
| `volume_mult` | 1.0 | Volume filter (1.0 = disabled, 1.2+ = require above-avg volume) |
| `volume_period` | 20 | Rolling window for volume average |
| `trade_start_hour` | 0 | Trade start hour UTC (0 = disabled, 6 = US/EU session) |
| `trade_end_hour` | 24 | Trade end hour UTC (24 = disabled, 22 = US/EU session) |
| `confirmation_candles` | 1 | Wait N candles after signal before entering (0 = immediate) |
| `vwap_slope_period` | 5 | Check VWAP slope over last N candles (0 = disabled) |
| `tp_atr_mult` | 1.5 | Take-profit = entry +/- 1.5 * ATR |
| `sl_atr_mult` | 1.0 | Stop-loss = entry +/- 1.0 * ATR |
| `swing_lookback` | 3 | Trailing stop = lowest low / highest high of last N candles |
| `risk_pct` | 0.01 | 1% of balance risked per trade (backtest only) |
| `trade_cooldown` | 60 | Minimum seconds between trades |
| `fetch_limit` | 1500 | Candles to fetch (must be >= vwap_window) |
