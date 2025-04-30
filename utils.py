import time

_last_trade_time = 0

def can_trade(cooldown):
    global _last_trade_time
    if time.time() - _last_trade_time >= cooldown:
        _last_trade_time = time.time()
        return True
    return False
