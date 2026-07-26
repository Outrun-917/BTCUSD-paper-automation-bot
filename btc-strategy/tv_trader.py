import logging
import time

import pyautogui

log = logging.getLogger(__name__)

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1

POSITIONS = {
    "buy_button": (-128, 250),
    "sell_button": (-291, 249),
    "tp_input_field": (-303, 519),
    "sl_input_field": (-132, 517),
    "confirm_button": (-205, 641),
    "close_position_button": (0, 0),  # calibrate with calibrate_coords.py
}

CLICK_DELAY = 0.5
MAX_RETRIES = 3


def _safe_click(position, label="button"):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            pyautogui.moveTo(position)
            time.sleep(0.1)
            pyautogui.click()
            log.debug("Clicked %s (attempt %d)", label, attempt)
            return True
        except Exception as e:
            log.warning("Click failed on %s (attempt %d): %s", label, attempt, e)
            time.sleep(0.3)
    log.error("All %d click attempts failed for %s", MAX_RETRIES, label)
    return False


def _type_field(position, value, label="field"):
    try:
        pyautogui.moveTo(position)
        time.sleep(0.1)
        pyautogui.click()
        time.sleep(0.2)
        pyautogui.hotkey("ctrl", "a")
        pyautogui.typewrite(f"{value:.2f}")
        log.debug("Typed %.2f into %s", value, label)
        return True
    except Exception as e:
        log.error("Typing failed on %s: %s", label, e)
        return False


def execute_trade(signal, current_price, tp_price, sl_price):
    log.info("Signal: %s @ %.2f  TP: %.2f  SL: %.2f", signal, current_price, tp_price, sl_price)

    if signal == "long":
        button_key = "buy_button"
    elif signal == "short":
        button_key = "sell_button"
    else:
        return False

    if not _safe_click(POSITIONS[button_key], button_key):
        return False
    time.sleep(CLICK_DELAY)

    if not _type_field(POSITIONS["tp_input_field"], tp_price, "TP"):
        return False
    time.sleep(0.2)

    if not _type_field(POSITIONS["sl_input_field"], sl_price, "SL"):
        return False
    time.sleep(0.2)

    if not _safe_click(POSITIONS["confirm_button"], "confirm"):
        return False

    log.info("Order placed: %s @ %.2f  TP %.2f  SL %.2f", signal.upper(), current_price, tp_price, sl_price)
    return True


def close_position():
    log.info("Closing position via TV...")
    if not _safe_click(POSITIONS["close_position_button"], "close_position"):
        log.error("Failed to close position on TradingView")
        return False
    time.sleep(CLICK_DELAY)
    log.info("Position closed on TradingView")
    return True
