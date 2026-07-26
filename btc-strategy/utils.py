import datetime
import time

_last_trade_time = 0


def can_trade(cooldown):
    global _last_trade_time
    return (time.time() - _last_trade_time) >= cooldown


def record_trade():
    global _last_trade_time
    _last_trade_time = time.time()


def seconds_until_next_candle():
    now = datetime.datetime.now()
    next_minute = (now + datetime.timedelta(minutes=1)).replace(second=0, microsecond=0)
    return max((next_minute - now).total_seconds(), 0)
