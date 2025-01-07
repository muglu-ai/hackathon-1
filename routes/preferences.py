from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User, Preference
from schemas import UserCreate, PreferenceCreate

router = APIRouter(prefix="/preferences", tags=["preferences"])

@router.post("/user/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    #new_user = User(email=user.email, language=user.language)
    print(user.username, user.email, user.language)
    new_user = User(email=user.email, language=user.language)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/set/")
def set_preferences(preference: PreferenceCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == preference.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    new_pref = Preference(user_id=preference.user_id, team=preference.team, player=preference.player)
    db.add(new_pref)
    db.commit()
    db.refresh(new_pref)
    return new_pref
