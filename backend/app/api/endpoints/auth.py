from fastapi import APIRouter, Depends, HTTPException, Response, status, Cookie
from sqlalchemy.orm import Session

# Используем точки, чтобы пути никогда не терялись на Windows
from ...api.deps import get_db, get_current_user
from ...core.security import get_password_hash, verify_password
from ...models.user import User
from ...schemas.user import UserCreate, UserRead, UserLogin

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """Регистрация нового пользователя"""
    user_exists = db.query(User).filter(User.email == user_in.email).first()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже зарегистрирован"
        )
    
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login")
def login(user_in: UserLogin, response: Response, db: Session = Depends(get_db)):
    """Вход в систему (установка Cookie)"""
    user = db.query(User).filter(User.username == user_in.username).first()
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверное имя пользователя или пароль"
        )
    
    response.set_cookie(
        key="session_id",
        value=str(user.id),
        httponly=True,
        max_age=3600,
        samesite="lax"
    )
    return {"message": "Успешный вход в систему"}

@router.post("/logout")
def logout(response: Response):
    """Выход из системы (удаление Cookie)"""
    response.delete_cookie(key="session_id")
    return {"message": "Успешный выход из системы"}

@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    """Проверка текущей сессии"""
    return current_user
