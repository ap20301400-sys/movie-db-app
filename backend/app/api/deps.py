from typing import Generator
from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.user import User

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    session_id: str | None = Cookie(default=None),
    db: Session = Depends(get_db)
) -> User:
    
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Вы не авторизованы (сессия отсутствует)"
        )
    
    user = db.query(User).filter(User.id == int(session_id)).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительная или устаревшая сессия"
        )
        
    return user
