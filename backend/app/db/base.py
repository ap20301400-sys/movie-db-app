# Импортируем Base и все модели для корректной инициализации через SQLAlchemy
from app.db.session import Base  # noqa
from app.models.user import User  # noqa
from app.models.watchlist import Watchlist  # noqa
from app.models.review import Review  # noqa

from app.db.session import engine

def init_db() -> None:
    # Эта команда создает все таблицы в файле sql_app.db, если их еще нет
    Base.metadata.create_all(bind=engine)
