from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import TransferBase
from models import Transfer
from datetime import date
from database import SessionLocal

router = APIRouter(prefix="/transfers", tags=["Transfers"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{user_id}")
def make_transfer(user_id: int, transfer: TransferBase, db: Session = Depends(get_db)):
    transfer_record = Transfer(
        user_id=user_id,
        player_out=transfer.player_out,
        player_in=transfer.player_in,
        timestamp=date.today()
    )
    db.add(transfer_record)
    db.commit()
    return {"message": "Transfer completed"}
