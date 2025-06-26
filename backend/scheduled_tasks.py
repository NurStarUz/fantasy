from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import pytz
from database import SessionLocal
from models import Player, PointsLog
from football_api import FootballDataAPI
from config import Config

def update_live_scores():
    tz = pytz.timezone(Config.TZ)
    db = SessionLocal()
    api = FootballDataAPI()
    
    try:
        print(f"Live score update started at {datetime.now(tz)}")
        
        matches = api.get_live_matches()
        for match in matches:
            events = api.get_match_events(match['id'])
            for event in events:
                self.process_event(event, match, db)
        
        db.commit()
        print("Live score update completed successfully")
    except Exception as e:
        db.rollback()
        print(f"Error in live update: {e}")
    finally:
        db.close()

def process_event(event, match, db):
    player_name = event.get('player', {}).get('name')
    if not player_name:
        return

    player = db.query(Player).filter(Player.name == player_name).first()
    if not player:
        return

    points_change = 0
    reason = ""
    
    event_type = event.get('type')
    if event_type == 'GOAL':
        points_change = 5
        reason = "goal"
        player.goals += 1
    elif event_type == 'ASSIST':
        points_change = 3
        reason = "assist"
        player.assists += 1
    # Add other event types...
    
    if points_change != 0:
        player.points += points_change
        log = PointsLog(
            player_id=player.id,
            points=points_change,
            reason=reason,
            value=points_change,
            match_id=match['id'],
            tournament=match['competition']['code']
        )
        db.add(log)

def init_scheduler():
    tz = pytz.timezone(Config.TZ)
    scheduler = BackgroundScheduler(timezone=tz)
    
    # Daily update at 07:00 Tashkent time
    scheduler.add_job(update_live_scores, 'cron', hour=7, minute=0)
    
    # Live updates every 5 minutes
    scheduler.add_job(update_live_scores, 'interval', minutes=5)
    
    scheduler.start()

if __name__ == "__main__":
    init_scheduler()
