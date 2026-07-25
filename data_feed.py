import logging

import ccxt
import pandas as pd

log = logging.getLogger(__name__)

exchange = ccxt.okx()


def fetch_candles(symbol="BTC/USD", timeframe="1m", limit=1500):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)
        return df
    except Exception as e:
        log.error("Failed to fetch candles: %s", e)
        return None
