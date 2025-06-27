from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import TeamBase
from models import Team
from database import SessionLocal

router = APIRouter(prefix="/teams", tags=["Teams"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{user_id}")
def set_team(user_id: int, team: TeamBase, db: Session = Depends(get_db)):
    player_ids_str = ",".join(map(str, team.player_ids))
    db_team = db.query(Team).filter(Team.user_id == user_id).first()
    if db_team:
        db_team.player_ids = player_ids_str
    else:
        db_team = Team(user_id=user_id, player_ids=player_ids_str)
        db.add(db_team)
    db.commit()
    return {"message": "Team saved successfully"}
