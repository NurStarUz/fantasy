from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True)
    full_name = Column(String)
    avatar = Column(String)

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    team = Column(String)
    position = Column(String)
    value = Column(Float)

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    player_ids = Column(String)  # Masalan: "11,12,13,..."

class Transfer(Base):
    __tablename__ = "transfers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    player_out = Column(Integer)
    player_in = Column(Integer)
    timestamp = Column(Date)

class PlayerPoints(Base):
    __tablename__ = "points"
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    match_date = Column(Date)
    goals = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    clean_sheet = Column(Integer, default=0)
    yellow_cards = Column(Integer, default=0)
    red_cards = Column(Integer, default=0)
    total_points = Column(Integer, default=0)
