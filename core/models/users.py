from .base import Base

from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped


class User(Base):
    
    username: Mapped[str] = mapped_column(String(64), unique=True)
    password: Mapped[bytes]
    email: Mapped[str] = mapped_column(unique=True)