import ta


def apply_indicators(df, atr_period=14):
    df = df.copy()

    df["atr"] = ta.volatility.AverageTrueRange(
        high=df["high"], low=df["low"], close=df["close"], window=atr_period
    ).average_true_range()

    return df
