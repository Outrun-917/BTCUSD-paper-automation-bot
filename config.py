import logging

CONFIG = {
    # --- Trading Pair ---
    "symbol": "NQ=F",
    "timeframe": "15m",

    # --- TJR: Swing Structure ---
    "swing_structure_period": 3,  # fractal N: swing high/low = highest/lowest in 2N+1 candle window
    "swing_lookback_sweep": 20,  # candles to scan for recent liquidity sweep
    "bos_lookback": 10,          # candles to scan for break of structure

    # --- Exit: Trailing Stop Only ---
    "sl_atr_mult": 1.5,          # initial stop-loss = entry +/- 1.5 * ATR (safety net)
    "swing_lookback": 3,         # trailing stop = lowest low / highest high of last N candles

    # --- Indicators (for position sizing only) ---
    "atr_period": 14,

    # --- Time-of-Day Filter (ET hours) ---
    "trade_start_hour": 8,       # 8:00 AM ET pre-market
    "trade_end_hour": 16,        # 4:00 PM ET market close

    # --- Risk / Sizing ---
    "risk_pct": 0.01,            # 1% of balance risked per trade

    # --- Mode ---
    "dry_run": True,

    # --- Timing ---
    "trade_cooldown": 300,       # seconds between trades (5 min for 15m candles)
    "fetch_limit": 500,          # candles to fetch

    # --- Logging ---
    "log_level": logging.INFO,
}
