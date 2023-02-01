from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base
from sqlalchemy.sql import func

from models.user import UserModel

chat_user = Table(
    'chat_user',
    Base.metadata,
    Column('chat_id', Integer, ForeignKey('chat.id')),
    Column('user_id', Integer, ForeignKey('user_table.id'))
)


class ChatModel(Base):
    __tablename__ = 'chat'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    is_group = Column(Boolean, nullable=False)
    members_array = relationship(
        'UserModel', secondary=chat_user, backref='chat')
    created_at = Column(String(255), nullable=False, server_default=func.now())

