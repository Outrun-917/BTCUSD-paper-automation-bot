from config import CONFIG


def _check_filters(df, side=None):
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

    # VWAP slope filter (skip if disabled)
    if side and CONFIG["vwap_slope_period"] > 0 and len(df) >= CONFIG["vwap_slope_period"]:
        n = CONFIG["vwap_slope_period"]
        vwap_now = df["vwap"].iloc[-1]
        vwap_prev = df["vwap"].iloc[-n]
        if side == "long" and vwap_now < vwap_prev:
            return False
        if side == "short" and vwap_now > vwap_prev:
            return False

    return True


def check_entry(df):
    conf = CONFIG["confirmation_candles"]

    if conf > 0 and len(df) < conf + 1:
        return None

    # Signal candle is N candles back, confirmation candle is the last candle
    signal_idx = -(conf + 1) if conf > 0 else -1
    confirm_idx = -1 if conf > 0 else -1

    signal = df.iloc[signal_idx]
    confirm = df.iloc[confirm_idx]

    # Long: RSI oversold + close below BB lower + below VWAP
    if (
        signal["rsi"] < CONFIG["rsi_oversold"] and
        signal["close"] < signal["bb_lower"] and
        signal["close"] < signal["vwap"]
    ):
        if conf > 0 and confirm["close"] < signal["close"]:
            return None
        if _check_filters(df, "long"):
            return "long"

    # Short: RSI overbought + close above BB upper + above VWAP
    if (
        signal["rsi"] > CONFIG["rsi_overbought"] and
        signal["close"] > signal["bb_upper"] and
        signal["close"] > signal["vwap"]
    ):
        if conf > 0 and confirm["close"] > signal["close"]:
            return None
        if _check_filters(df, "short"):
            return "short"

    return None
