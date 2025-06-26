from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime
from database import Base
from config import Config
import pytz

class Player(Base):
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    position = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    team = Column(String, nullable=False)
    points = Column(Integer, default=0)
    goals = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    clean_sheets = Column(Integer, default=0)
    yellow_cards = Column(Integer, default=0)
    red_cards = Column(Integer, default=0)
    tournament = Column(String, nullable=False)
    last_updated = Column(DateTime, default=datetime.now(pytz.timezone(Config.TZ)))

class UserTeam(Base):
    __tablename__ = "user_teams"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String)
    budget = Column(Float, default=100.0)
    weekly_transfers = Column(Integer, default=1)
    total_points = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.now(pytz.timezone(Config.TZ)))

class TeamPlayer(Base):
    __tablename__ = "team_players"
    
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey('user_teams.id'))
    player_id = Column(Integer, ForeignKey('players.id'))

class PointsLog(Base):
    __tablename__ = "points_logs"
    
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    team_id = Column(Integer, ForeignKey('user_teams.id'))
    points = Column(Integer)
    reason = Column(String)
    value = Column(Integer)
    match_id = Column(String)
    tournament = Column(String)
    created_at = Column(DateTime, default=datetime.now(pytz.timezone(Config.TZ)))
