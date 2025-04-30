import os
from dotenv import load_dotenv

load_dotenv()

CONFIG = {
    "exchange": "OKX",
    "symbol": "BTC/USD",
    "timeframe": "1m",
    "rsi_period": 14,
    "bollinger_period": 20,
    "bollinger_dev": 2,
    "trade_cooldown": 60,  # seconds
    "sl_pct": 0.002,
    "tp_pct": 0.003,
    "risk_pct": 0.01,
    "apiKey": os.getenv("OKX_API_KEY"),
    "secret": os.getenv("OKX_SECRET"),
    "password": os.getenv("OKX_PASSWORD"),
    "browser_path": "C:/Program Files/Google/Chrome/Application/chrome.exe"
}
