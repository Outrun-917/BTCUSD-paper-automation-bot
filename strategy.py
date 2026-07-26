from config import CONFIG


def find_swings(df, period, start_idx=0):
    """Find swing highs and lows using fractal logic from start_idx onwards.

    A swing high at index i: high[i] is the highest high in [i-period, i+period].
    A swing low at index i: low[i] is the lowest low in [i-period, i+period].

    Only returns confirmed swings (i+period < len(df)).
    """
    swing_highs = []
    swing_lows = []
    end = len(df) - period

    for i in range(max(period, start_idx), end):
        window_highs = df["high"].iloc[i - period: i + period + 1]
        window_lows = df["low"].iloc[i - period: i + period + 1]

        if df["high"].iloc[i] == window_highs.max():
            swing_highs.append((df.index[i], df["high"].iloc[i]))

        if df["low"].iloc[i] == window_lows.min():
            swing_lows.append((df.index[i], df["low"].iloc[i]))

    return swing_highs, swing_lows


def check_entry(df):
    """Pure TJR entry: liquidity sweep + break of structure (BOS).

    Long entry: sweep below swing low + BOS above swing high
    Short entry: sweep above swing high + BOS below swing low
    """
    period = CONFIG["swing_structure_period"]
    bos_lb = CONFIG["bos_lookback"]
    sweep_lb = CONFIG["swing_lookback_sweep"]
    min_len = period * 2 + 2

    if len(df) < min_len:
        return None

    # Find swings — only scan the tail of the dataframe for efficiency
    scan_start = max(0, len(df) - sweep_lb - period * 2 - 10)
    all_highs, all_lows = find_swings(df, period, start_idx=scan_start)

    if not all_highs or not all_lows:
        return None

    # Most recent confirmed swing high/low within BOS lookback
    last_ts = df.index[-1]
    recent_high = None
    for ts, price in reversed(all_highs):
        gap = len(df.loc[ts:last_ts]) - 1
        if gap <= bos_lb:
            recent_high = (ts, price)
            break

    recent_low = None
    for ts, price in reversed(all_lows):
        gap = len(df.loc[ts:last_ts]) - 1
        if gap <= bos_lb:
            recent_low = (ts, price)
            break

    # Wider scan for sweep context
    sweep_high = None
    for ts, price in reversed(all_highs):
        gap = len(df.loc[ts:last_ts]) - 1
        if gap <= sweep_lb:
            sweep_high = (ts, price)
            break

    sweep_low = None
    for ts, price in reversed(all_lows):
        gap = len(df.loc[ts:last_ts]) - 1
        if gap <= sweep_lb:
            sweep_low = (ts, price)
            break

    if sweep_low is None and sweep_high is None:
        return None

    # Check for sweep in the last N candles
    n = min(sweep_lb, len(df) - 1)
    sweep_side = None
    sweep_price = None

    for i in range(len(df) - n, len(df)):
        candle = df.iloc[i]

        if sweep_low is not None and candle["low"] < sweep_low[1] and candle["close"] > sweep_low[1]:
            sweep_side = "long"
            sweep_price = sweep_low[1]
            break

        if sweep_high is not None and candle["high"] > sweep_high[1] and candle["close"] < sweep_high[1]:
            sweep_side = "short"
            sweep_price = sweep_high[1]
            break

    if sweep_side is None:
        return None

    last = df.iloc[-1]

    # Time filter
    hour = df.index[-1].hour
    if not (CONFIG["trade_start_hour"] <= hour < CONFIG["trade_end_hour"]):
        return None

    if sweep_side == "long":
        if recent_high is not None and last["close"] > recent_high[1]:
            return "long"

    elif sweep_side == "short":
        if recent_low is not None and last["close"] < recent_low[1]:
            return "short"

    return None
