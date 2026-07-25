# BTCUSD Auto Scalper Bot (Visual Paper Trading via TradingView)

> **Disclaimer:** Experimental bot. Do not use with real money.

## Description

- Fetches BTC/USD 1m candles from OKX via `ccxt`
- Technical indicators: RSI, Bollinger Bands, Rolling VWAP (24h), ATR
- Entry signals: RSI extreme + BB band break + VWAP confluence
- Exit: ATR-based TP/SL with trailing stop
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
| `vwap_window` | 1440 | Rolling VWAP window (1440 = 24h of 1m candles) |
| `atr_period` | 14 | ATR period |
| `rsi_oversold` | 28 | Long entry threshold |
| `rsi_overbought` | 72 | Short entry threshold |
| `tp_atr_mult` | 2.5 | Take-profit = entry +/- 2.5 * ATR |
| `sl_atr_mult` | 1.5 | Stop-loss = entry +/- 1.5 * ATR |
| `trail_activate_atr` | 1.0 | Trailing stop activates after 1.0 * ATR move |
| `trail_sl_atr` | 1.0 | Trailing SL follows at 1.0 * ATR behind best price |
| `trade_cooldown` | 60 | Minimum seconds between trades |
| `fetch_limit` | 1500 | Candles to fetch (must be >= vwap_window) |
