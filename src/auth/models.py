from pydantic import EmailStr
from sqlalchemy import Column, String, Boolean, Integer
from fastapi_users.db import SQLAlchemyBaseUserTable
from src.database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True)
    email: EmailStr = Column(String(length=255), unique=True, index=True, nullable=False)
    username: str = Column(String, nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
