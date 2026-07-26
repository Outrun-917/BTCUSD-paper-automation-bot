import pandas as pd
import ta


def apply_indicators(df, vwap_window=1440, atr_period=14, bb_period=20, bb_dev=2,
                     volume_period=20):
    df = df.copy()

    # RSI
    df["rsi"] = ta.momentum.RSIIndicator(close=df["close"]).rsi()

    # Bollinger Bands
    boll = ta.volatility.BollingerBands(close=df["close"], window=bb_period, window_dev=bb_dev)
    df["bb_upper"] = boll.bollinger_hband()
    df["bb_lower"] = boll.bollinger_lband()

    # Rolling VWAP (24h window)
    typical_price = (df["high"] + df["low"] + df["close"]) / 3
    vol_tp = typical_price * df["volume"]
    df["vwap"] = vol_tp.rolling(window=vwap_window).sum() / df["volume"].rolling(window=vwap_window).sum()

    # ATR
    df["atr"] = ta.volatility.AverageTrueRange(
        high=df["high"], low=df["low"], close=df["close"], window=atr_period
    ).average_true_range()

    # Volume average
    df["vol_avg"] = df["volume"].rolling(window=volume_period).mean()

    return df
