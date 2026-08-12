from datetime import datetime
from sqlalchemy import Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base

class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    tmdb_movie_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)  # Валидацию от 1 до 10 сделаем позже в Pydantic-схемах
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    # Обратная связь с пользователем
    user: Mapped["User"] = relationship(back_populates="reviews")
