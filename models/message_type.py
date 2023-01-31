from sqlalchemy import Column, Integer, String
from database.base import Base

class MessageTypeModel(Base):
    __tablename__ = 'message_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    mime = Column(String(255), nullable=False)