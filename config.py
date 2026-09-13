import os
from dotenv import load_dotenv

load_dotenv()

MIN_SCORE = int(os.getenv("MIN_SCORE", "80"))
MIN_RR = float(os.getenv("MIN_RR", "2.0"))
SCAN_INTERVAL_MINUTES = int(os.getenv("SCAN_INTERVAL_MINUTES", "15"))

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
