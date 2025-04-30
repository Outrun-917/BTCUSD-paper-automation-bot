import pyautogui
import time

# You must manually open TradingView to paper account and position the screen
def click_button(label):
    print(f"[Action] Clicking {label} button (calibrate position manually)")
    if label == "buy":
        pyautogui.moveTo(1600, 950)  # <-- ADJUST THIS TO YOUR BUY BUTTON COORDINATE
    elif label == "sell":
        pyautogui.moveTo(1700, 950)  # <-- ADJUST TO YOUR SELL BUTTON
    pyautogui.click()

def open_browser():
    import subprocess
    from config import CONFIG
    subprocess.Popen([CONFIG["browser_path"], "https://fr.tradingview.com/chart/S7WFULlf/"])

def execute_trade(signal):
    if signal == "long":
        click_button("buy")
    elif signal == "short":
        click_button("sell")
