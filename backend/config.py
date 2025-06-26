import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://nurstar:9zM1pSmDMwO3fKovJ2hQlyQbnxZSVHDW@dpg-d1eegdp5pdvs73bvi4jg-a/fantasydb_tise")
    FOOTBALL_API_KEY = os.getenv("bbb143c3e3834132934ccf14fa9343ea")
    TELEGRAM_BOT_TOKEN = os.getenv("7810185081:AAHX-vIcHd8_2kwlEUoq6_BBpeQ5cTLWMGM")
    TZ = os.getenv("TZ", "Asia/Tashkent")
