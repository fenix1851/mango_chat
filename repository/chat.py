from models.chat import ChatModel
from models.user import UserModel
from fastapi import Response, HTTPException, Depends, status, Cookie
from repository.base import BaseRepository
from schemas.chat import ChatBaseSchema, ChatUpdateSchema

class ChatRepository(BaseRepository):
    async def get_chats(self, user):
        # members of chats stored in array in chat model
        # so we need to get all chats
        user = self.session.query(UserModel).filter_by(id=user.id).first()
        chats = user.chat
        for chat in chats:
            chat = self.session.query(ChatModel).filter_by(id=chat.id).first()
        print(chats)
        return chats
    async def get_by_id(self, id, user):
        user = self.session.query(UserModel).filter_by(id=user.id).first()
        chat = self.session.query(ChatModel).filter_by(id=id).first()
        if chat not in user.chat:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
        return chat
    async def create(self, user, data:dict):
        # try to get chat with same name if so return error
        chat = self.session.query(ChatModel).filter_by(name=data['name']).first()
        if chat:
            return 'Chat already exists'
        members = data["members_array"]
        members.append(user.id)
        members = list(set(members))
        for index,member in enumerate(members):
            members[index] = self.session.query(UserModel).filter_by(id=member).first()
            if not member:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        data['members_array'] = members
        chat = ChatModel(**data)
        self.session.add(chat)
        self.session.commit()
        return {'chat': chat, 'members_array': members, "id": chat.id}