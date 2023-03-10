from sqlalchemy import Column, Integer, String, ForeignKey, ARRAY, Table
from database.base import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from models.user import UserModel
from models.message_type import MessageTypeModel

message_likes = Table(
    'message_likes',
    Base.metadata,
    Column('message_id', Integer, ForeignKey('message.id')),
    Column('user_id', Integer, ForeignKey('user_table.id'))
)

class MessageModel(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True, autoincrement=True)
    likes_array = relationship(
        "UserModel", backref="message_likes", secondary="message_likes")
    user_id = Column(Integer, ForeignKey('user_table.id'))
    chat_id = Column(Integer, ForeignKey('chat.id'))
    message_type = Column(Integer, ForeignKey('message_type.id'))
    content = Column(String(255), nullable=False)   
    created_at = Column(String(255), nullable=False, server_default=func.now())
    