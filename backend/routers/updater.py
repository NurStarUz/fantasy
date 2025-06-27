from fastapi import APIRouter
import httpx
import os
from datetime import date
from database import SessionLocal
from models import PlayerPoints

router = APIRouter(prefix="/update", tags=["Update"])

@router.post("/points")
async def update_points():
    token = os.getenv("FOOTBALL_API_TOKEN")
    headers = {"X-Auth-Token": token}
    leagues = ["PL", "PD", "SA", "BL1", "FL1", "CL", "EL", "WC", "EC", "WC-Q", "CWC"]
    today = date.today().isoformat()

    db = SessionLocal()
    for league in leagues:
        url = f"https://api.football-data.org/v4/competitions/{league}/matches?dateFrom={today}&dateTo={today}"
        async with httpx.AsyncClient() as client:
            res = await client.get(url, headers=headers)
        matches = res.json().get("matches", [])
        for match in matches:
            # Simulyatsiya: haqiqiy statistikalar to‘liq emas, soxta qiymatlar
            for player_id in range(1, 16):
                points = PlayerPoints(
                    player_id=player_id,
                    match_date=date.today(),
                    goals=1,
                    assists=1,
                    clean_sheet=1,
                    yellow_cards=0,
                    red_cards=0,
                    total_points=13
                )
                db.add(points)
    db.commit()
    db.close()
    return {"message": "Points updated"}
