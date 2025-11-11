import os
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("USER_CHAT_ID")

BOT = Bot(token=TOKEN)

ASSETS = {
    "S&P 500": "^GSPC",
    "NASDAQ": "^IXIC",
    "MSCI World": "URTH",
    "MSCI Emerging Markets": "EEM",
    "Oro": "GC=F",
    "Plata": "SI=F",
    "Bitcoin": "BTC-EUR"
}

# Umbrales
UMBRAL_NORMAL = 1.0
UMBRAL_EXTREMO = 2.5
UMBRAL_NORMAL_CRYPTO = 3.0
UMBRAL_EXTREMO_CRYPTO = 6.0