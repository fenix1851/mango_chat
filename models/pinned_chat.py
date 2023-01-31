from sqlalchemy import Column,  ForeignKey, ARRAY, Integer, String, Table
from database.base import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from models.user import UserModel
from models.chat import ChatModel

pinnded_chat_chats = Table(
    'pinned_chat_chats',
    Base.metadata,
    Column('pinned_chat_id', Integer, ForeignKey('pinned_chat.id')),
    Column('chat_id', Integer, ForeignKey('chat.id'))
)


class PinnedChatModel(Base):
    __tablename__ = 'pinned_chat'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(Integer, ForeignKey('user.id'))
    chats_array = relationship(
        'ChatModel', secondary=pinnded_chat_chats, back_populates='pinned_chat')


    created_at = Column(String(255), nullable=False, server_default=func.now())
