import logging

CONFIG = {
    # --- Trading Pair ---
    "symbol": "BTC/USD",
    "timeframe": "5m",

    # --- Indicators ---
    "rsi_period": 14,
    "bollinger_period": 20,
    "bollinger_dev": 2,
    "vwap_window": 288,        # 24h rolling window (288 x 5m candles)
    "atr_period": 14,

    # --- Entry Thresholds ---
    "rsi_oversold": 32,
    "rsi_overbought": 68,

    # --- Volume Filter ---
    "volume_mult": 1.0,          # disabled (set 1.2+ to require above-avg volume)
    "volume_period": 20,         # rolling window for volume average

    # --- Time-of-Day Filter (UTC hours) ---
    "trade_start_hour": 0,       # disabled (set 6-22 to filter to US/EU session)
    "trade_end_hour": 24,

    # --- Confirmation Filters ---
    "confirmation_candles": 1,   # wait N candles after signal before entering (0 = immediate)
    "vwap_slope_period": 5,      # check VWAP slope over last N candles (0 = disabled)

    # --- Exit: ATR-Based TP/SL ---
    "tp_atr_mult": 1.5,        # take-profit = entry ± 1.5 * ATR
    "sl_atr_mult": 1.0,        # stop-loss  = entry ± 1.0 * ATR

    # --- Trailing Stop (swing-based) ---
    "swing_lookback": 3,         # trailing stop = lowest low of last N candles

    # --- Risk / Sizing ---
    "risk_pct": 0.01,           # 1% of balance risked per trade (backtest only)

    # --- Timing ---
    "trade_cooldown": 60,       # seconds between trades
    "fetch_limit": 1500,        # candles to fetch (needs >= vwap_window + atr_period)

    # --- Mode ---
    "dry_run": True,             # True = simulate trades locally, False = execute on TradingView via pyautogui

    # --- Logging ---
    "log_level": logging.INFO,
}
