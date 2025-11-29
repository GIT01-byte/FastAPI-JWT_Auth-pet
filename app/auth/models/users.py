
from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base

class UsersOrm(Base):
    __tablename__ = 'users' 
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[bytes] = mapped_column(unique=True, nullable=False)
    email: Mapped[str | None] = mapped_column(unique=True)
    avatar_links: Mapped[str | None]
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
