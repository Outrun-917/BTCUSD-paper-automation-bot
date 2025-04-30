import ccxt
from config import CONFIG
import pandas as pd
from datetime import datetime

def get_okx_client():
    return ccxt.okx({
        'apiKey': CONFIG["apiKey"],
        'secret': CONFIG["secret"],
        'password': CONFIG["password"],
        'enableRateLimit': True,
        'options': {'defaultType': 'future'}
    })

def fetch_candles(client, symbol="BTC/USD", timeframe="1m", limit=100):
    ohlcv = client.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    return df
