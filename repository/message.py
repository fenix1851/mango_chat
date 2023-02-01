from models.message import MessageModel
from models.user import UserModel
from repository.base import BaseRepository
from fastapi import Response, HTTPException

class MessageRepository(BaseRepository):
    async def get_messages(self, chat_id, user):
        # check if user is member of chat
        user = self.session.query(UserModel).filter_by(id=user.id).first()
        chats = user.chat
        for chat in chats:
            if chat.id == chat_id:
                messages = self.session.query(MessageModel).filter_by(chat_id=chat_id).all()
                return messages
        raise HTTPException(status_code=404, detail="Chat not found")