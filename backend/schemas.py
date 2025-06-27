from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class UserBase(BaseModel):
    telegram_id: str
    full_name: Optional[str]
    avatar: Optional[str]

class TeamBase(BaseModel):
    player_ids: List[int]

class TransferBase(BaseModel):
    player_out: int
    player_in: int

class PlayerPoint(BaseModel):
    player_id: int
    match_date: date
    goals: int
    assists: int
    clean_sheet: int
    yellow_cards: int
    red_cards: int
    total_points: int  # Bu yerda muammo yo'q
