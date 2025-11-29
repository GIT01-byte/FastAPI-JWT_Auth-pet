from typing import Any
from sqlalchemy import Integer, String, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base

class UsersOrm(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[bytes] = mapped_column(nullable=False)
    email: Mapped[str | None] = mapped_column(String, unique=True)
    profile: Mapped[Any | None] = mapped_column(JSON)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
