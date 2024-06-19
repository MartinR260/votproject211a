from sqlalchemy import Text, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Leaderboard(Base):
    __tablename__ = "leaderboard"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(Text)
    name: Mapped[str] = mapped_column(Text)
    best_score: Mapped[int] = mapped_column(Integer)
    date_time: Mapped[DateTime] = mapped_column(DateTime)

    def __init__(self, user_id, name, best_score):
        self.user_id = user_id
        self.name = name
        self.best_score = best_score
        self.date_time = datetime.now()