import requests
from config import Config
from datetime import datetime, timedelta
import pytz

class FootballDataAPI:
    BASE_URL = "https://api.football-data.org/v4"
    SUPPORTED_COMPETITIONS = {
        'UCL': 'CL',  # Champions League
        'UEL': 'EL',  # Europa League
        'UECL': 'ECL',  # Conference League
        'WC': 'WC',  # World Cup
        'CWC': 'CWC',  # Club World Cup
        'EPL': 'PL',  # Premier League
        'LL': 'PD',  # La Liga
        'BL': 'BL1',  # Bundesliga
        'SA': 'SA',  # Serie A
        'L1': 'FL1',  # Ligue 1
        'WCQ': 'WCQ',  # World Cup Qualifiers
        'EQC': 'ECQ',  # Euro Qualifiers
        'SC': 'SC'  # Super Cup
    }

    def __init__(self):
        self.headers = {'X-Auth-Token': Config.FOOTBALL_API_KEY}
        self.tz = pytz.timezone(Config.TZ)

    def get_live_matches(self):
        date_from = (datetime.now(self.tz) - timedelta(days=1)).strftime('%Y-%m-%d')
        date_to = (datetime.now(self.tz) + timedelta(days=1)).strftime('%Y-%m-%d')
        
        matches = []
        for code in self.SUPPORTED_COMPETITIONS.values():
            url = f"{self.BASE_URL}/competitions/{code}/matches?dateFrom={date_from}&dateTo={date_to}"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                matches.extend(response.json().get('matches', []))
        return matches

    def get_match_events(self, match_id):
        url = f"{self.BASE_URL}/matches/{match_id}/events"
        response = requests.get(url, headers=self.headers)
        return response.json().get('events', []) if response.status_code == 200 else []
