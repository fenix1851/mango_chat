from sqlalchemy import Column, Integer, String, ForeignKey
from database.base import Base
from sqlalchemy.sql import func

class UserModel(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    phone = Column(String(30), nullable=False)
    # photo - path to photo in storage
    photo = Column(String(255), nullable=False)
    description = Column(String(255))
    hashed_password = Column(String(255), nullable=False)
    refresh_token = Column(String(255))
    created_at = Column(String(255), nullable=False, server_default=func.now())