import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/fantasy_football")
    FOOTBALL_API_KEY = os.getenv("FOOTBALL_API_KEY")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TZ = os.getenv("TZ", "Asia/Tashkent")
