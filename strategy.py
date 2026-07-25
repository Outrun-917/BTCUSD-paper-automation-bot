from config import CONFIG


def _check_filters(df):
    last = df.iloc[-1]

    # Volume filter (skip if disabled)
    if CONFIG["volume_mult"] > 1.0:
        if last["vol_avg"] > 0 and last["volume"] < CONFIG["volume_mult"] * last["vol_avg"]:
            return False

    # Time-of-day filter (skip if full day range)
    if CONFIG["trade_start_hour"] != 0 or CONFIG["trade_end_hour"] != 24:
        hour = df.index[-1].hour
        if not (CONFIG["trade_start_hour"] <= hour < CONFIG["trade_end_hour"]):
            return False

    return True


def check_entry(df):
    if not _check_filters(df):
        return None

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
