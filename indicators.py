import pandas as pd
import ta

def apply_indicators(df):
    df = df.copy()
    df["rsi"] = ta.momentum.RSIIndicator(close=df["close"]).rsi()
    boll = ta.volatility.BollingerBands(close=df["close"])
    df["bb_upper"] = boll.bollinger_hband()
    df["bb_lower"] = boll.bollinger_lband()
    df["vwap"] = (df["volume"] * (df["high"] + df["low"] + df["close"]) / 3).cumsum() / df["volume"].cumsum()
    return df
