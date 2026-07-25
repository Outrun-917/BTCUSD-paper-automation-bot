import logging

import ccxt
import pandas as pd

log = logging.getLogger(__name__)

exchange = ccxt.okx()

OKX_MAX = 300


def fetch_candles(symbol="BTC/USD", timeframe="1m", limit=1500):
    try:
        all_candles = []
        after = None
        remaining = limit

        while remaining > 0:
            batch = min(remaining, OKX_MAX)
            params = {"after": after} if after else {}
            candles = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=batch, params=params)
            if not candles:
                break
            all_candles = candles + all_candles
            after = candles[0][0]
            remaining -= len(candles)
            if len(candles) < batch:
                break

        df = pd.DataFrame(all_candles, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)
        df = df[~df.index.duplicated(keep="first")]
        return df
    except Exception as e:
        log.error("Failed to fetch candles: %s", e)
        return None
