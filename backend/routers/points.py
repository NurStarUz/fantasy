from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import PlayerPoints, Team
from database import SessionLocal
from datetime import date

router = APIRouter(prefix="/points", tags=["Points"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/team/{user_id}")
def get_team_points(user_id: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.user_id == user_id).first()
    if not team:
        return {"points": 0, "details": []}
    player_ids = list(map(int, team.player_ids.split(',')))
    today = date.today()
    player_points = db.query(PlayerPoints).filter(
        PlayerPoints.player_id.in_(player_ids),
        PlayerPoints.match_date == today
    ).all()

    total = sum(p.total_points for p in player_points)
    details = [
        {
            "player_id": p.player_id,
            "goals": p.goals,
            "assists": p.assists,
            "clean_sheet": p.clean_sheet,
            "yellow_cards": p.yellow_cards,
            "red_cards": p.red_cards,
            "points": p.total_points
        } for p in player_points
    ]
    return {"total_points": total, "details": details}
