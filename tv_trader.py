import pyautogui
import time

POSITIONS = {
    "buy_button": (2439, 252),
    "sell_button": (2255, 251),
    "tp_input_field": (2263, 579),
    "sl_input_field": (2435, 580),
    "confirm_button": (2353, 644),
}

def type_field(position, value):
    pyautogui.moveTo(position)
    pyautogui.click()
    time.sleep(0.3)
    pyautogui.hotkey("ctrl", "a")
    pyautogui.typewrite(f"{value:.2f}")

def execute_trade(signal, current_price, tp_pct, sl_pct):
    print(f"[TV TRADE] Signal: {signal} @ {current_price}")

    # Calculate actual prices
    if signal == "long":
        tp = current_price * (1 + tp_pct)
        sl = current_price * (1 - sl_pct)
        pyautogui.moveTo(POSITIONS["buy_button"])
    elif signal == "short":
        tp = current_price * (1 - tp_pct)
        sl = current_price * (1 + sl_pct)
        pyautogui.moveTo(POSITIONS["sell_button"])
    else:
        return

    pyautogui.click()
    time.sleep(0.5)

    type_field(POSITIONS["tp_input_field"], tp)
    type_field(POSITIONS["sl_input_field"], sl)

    pyautogui.moveTo(POSITIONS["confirm_button"])
    pyautogui.click()

    print(f"[TV TRADE] TP: {tp:.2f}, SL: {sl:.2f} — Order Placed")
