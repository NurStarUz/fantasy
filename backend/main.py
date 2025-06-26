from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from models import Player, UserTeam, TeamPlayer, PointsLog
from database import Base, engine, get_db
from typing import List
from pydantic import BaseModel
from datetime import datetime
import pytz
from config import Config
from scheduled_tasks import init_scheduler

app = FastAPI()

# Initialize database
Base.metadata.create_all(bind=engine)

# Start scheduler
init_scheduler()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class PlayerBase(BaseModel):
    id: int
    name: str
    position: str
    price: float
    team: str
    points: int
    goals: int
    assists: int
    tournament: str

class TeamCreate(BaseModel):
    user_id: int
    name: str

class TransferRequest(BaseModel):
    team_id: int
    player_out_id: int
    player_in_id: int

class PointsLogResponse(BaseModel):
    date: str
    reason: str
    points: int
    description: str
    match_id: str
    tournament: str

# API Endpoints
@app.get("/players", response_model=List[PlayerBase])
def get_players(db: Session = Depends(get_db)):
    return db.query(Player).all()

@app.post("/teams/")
def create_team(team: TeamCreate, db: Session = Depends(get_db)):
    db_team = UserTeam(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

@app.get("/teams/{user_id}")
def get_user_team(user_id: int, db: Session = Depends(get_db)):
    team = db.query(UserTeam).filter(UserTeam.user_id == user_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@app.get("/points-history/{team_id}")
def get_points_history(team_id: int, db: Session = Depends(get_db)):
    logs = db.query(PointsLog).filter(PointsLog.team_id == team_id).all()
    
    return [{
        "date": log.created_at.strftime("%Y-%m-%d %H:%M"),
        "reason": log.reason,
        "points": log.points,
        "description": get_reason_description(log.reason),
        "match_id": log.match_id,
        "tournament": log.tournament
    } for log in logs]

def get_reason_description(reason):
    descriptions = {
        "goal": "⚽ Gol urish",
        "assist": "🎯 Golli uzatma",
        "clean_sheet": "🧤 Quruq darvozabon",
        "yellow_card": "🟨 Sariq kartochka",
        "red_card": "🟥 Qizil kartochka",
        "penalty_save": "🧤 Penaltini qaytarish",
        "own_goal": "❌ Avtogol",
        "motm": "⭐ Eng yaxshi futbolchi"
    }
    return descriptions.get(reason, reason)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
