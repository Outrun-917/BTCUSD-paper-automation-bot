import logging

CONFIG = {
    # --- Trading Pair ---
    "symbol": "BTC/USD",
    "timeframe": "1m",

    # --- Indicators ---
    "rsi_period": 14,
    "bollinger_period": 20,
    "bollinger_dev": 2,
    "vwap_window": 1440,       # 24h rolling window (1440 x 1m candles)
    "atr_period": 14,

    # --- Entry Thresholds ---
    "rsi_oversold": 28,
    "rsi_overbought": 72,

    # --- Exit: ATR-Based TP/SL ---
    "tp_atr_mult": 2.5,        # take-profit = entry ± 2.5 * ATR
    "sl_atr_mult": 1.5,        # stop-loss  = entry ± 1.5 * ATR

    # --- Trailing Stop ---
    "trail_activate_atr": 1.0,  # activate trailing after price moves 1.0 * ATR in favour
    "trail_sl_atr": 1.0,        # trail SL at 1.0 * ATR behind best price

    # --- Risk / Sizing ---
    "risk_pct": 0.01,           # 1% of balance risked per trade (backtest only)

    # --- Timing ---
    "trade_cooldown": 60,       # seconds between trades
    "fetch_limit": 1500,        # candles to fetch (needs >= vwap_window + atr_period)

    # --- Logging ---
    "log_level": logging.INFO,
}
