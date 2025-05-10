import ccxt
import pandas as pd

exchange = ccxt.okx()

def fetch_candles(symbol="BTC/USD", timeframe="1m", limit=100):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])  # ✅ 6 columns only
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)
        return df
    except Exception as e:
        print(f"[ERROR] Failed to fetch candles: {e}")
        return None