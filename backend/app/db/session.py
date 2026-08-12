from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# 1. URL для подключения к базе данных SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# 2. Создаем движок (create_engine) с параметром check_same_thread=False
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# 3. Настраиваем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Настраиваем базовый класс DeclarativeBase
class Base(DeclarativeBase):
    pass
