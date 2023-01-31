from sqlalchemy import Column, Integer, String, ForeignKey, ARRAY, Table
from database.base import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from models.user import UserModel

message_likes = Table(
    'message_likes',
    Base.metadata,
    Column('message_id', Integer, ForeignKey('message.id')),
    Column('user_id', Integer, ForeignKey('user.id'))
)

class MessageModel(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True, autoincrement=True)
    likes_array = relationship(
        "UserModel", back_populates="message_likes", secondary="message_likes")
    user_id = Column(Integer, ForeignKey('user.id'))
    chat_id = Column(Integer, ForeignKey('chat.id'))
    type = Column(String(255), nullable=False)
    created_at = Column(String(255), nullable=False, server_default=func.now())
