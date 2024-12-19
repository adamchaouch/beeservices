from sqlalchemy import Column, Integer, String, Enum
from app.db.session import Base
from enum import Enum as PyEnum

class UserType(PyEnum):
    PROVIDER = "provider"
    REQUESTER = "requester"
    HR_PRO = "hr_pro"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    user_type = Column(Enum(UserType), nullable=False)
