from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import UserBase
from models import User
from database import SessionLocal

router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def register_user(user: UserBase, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.telegram_id == user.telegram_id).first()
    if not db_user:
        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return db_user
