def check_entry(df):
    last = df.iloc[-1]
    if (
        last["rsi"] < 28 and
        last["close"] < last["bb_lower"] and
        last["close"] < last["vwap"]
    ):
        return "long"

    if (
        last["rsi"] > 72 and
        last["close"] > last["bb_upper"] and
        last["close"] > last["vwap"]
    ):
        return "short"

    return None
