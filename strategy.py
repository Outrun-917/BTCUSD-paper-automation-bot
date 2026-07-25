from config import CONFIG


def check_entry(df):
    last = df.iloc[-1]
    if (
        last["rsi"] < CONFIG["rsi_oversold"] and
        last["close"] < last["bb_lower"] and
        last["close"] < last["vwap"]
    ):
        return "long"

    if (
        last["rsi"] > CONFIG["rsi_overbought"] and
        last["close"] > last["bb_upper"] and
        last["close"] > last["vwap"]
    ):
        return "short"

    return None
