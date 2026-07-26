import logging

import pandas as pd
import yfinance as yf

log = logging.getLogger(__name__)


def fetch_candles(symbol="NQ=F", timeframe="15m", limit=500):
    try:
        ticker = yf.Ticker(symbol)

        # yfinance limits: 1m=7d, 5m=60d, 15m=60d, 1h=730d, 1d=unlimited
        tf_map = {
            "1m": ("1m", "7d"),
            "5m": ("5m", "60d"),
            "15m": ("15m", "60d"),
            "30m": ("30m", "60d"),
            "1h": ("1h", "730d"),
            "1d": ("1d", "10y"),
        }

        if timeframe not in tf_map:
            log.error("Unsupported timeframe: %s", timeframe)
            return None

        interval, period = tf_map[timeframe]
        df = ticker.history(period=period, interval=interval)

        if df.empty:
            log.warning("No data returned for %s", symbol)
            return None

        # Standardize columns
        df = df.rename(columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
        })

        df = df[["open", "high", "low", "close", "volume"]]
        df.index.name = "timestamp"

        # Trim to requested limit
        if len(df) > limit:
            df = df.iloc[-limit:]

        log.info("Fetched %d candles for %s (%s)", len(df), symbol, timeframe)
        return df

    except Exception as e:
        log.error("Failed to fetch candles: %s", e)
        return None
