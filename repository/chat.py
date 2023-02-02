from models.chat import ChatModel
from models.user import UserModel
from models.pinned_chat import PinnedChatModel
from fastapi import Response, HTTPException, Depends, status, Cookie
from repository.base import BaseRepository
from schemas.chat import ChatBaseSchema, ChatUpdateSchema
from loguru import logger

class ChatRepository(BaseRepository):
    async def get_chats(self, user):
        # members of chats stored in array in chat model
        # so we need to get all chats
        user = self.session.query(UserModel).filter_by(id=user.id).first()
        logger.info('Getting chats for user: ', user)
        chats = user.chat
        for chat in chats:
            chat = self.session.query(ChatModel).filter_by(id=chat.id).first()
        logger.info(f'Chats for user: {user} are: {chats}')
        return chats
    
    async def get_by_id(self, id, user):
        logger.info(f'Getting chat by id: {id} for user: {user}')
        user = self.session.query(UserModel).filter_by(id=user.id).first()
        logger.info('Getting chats for user: ', user)
        chat = self.session.query(ChatModel).filter_by(id=id).first()
        logger.info(f'Chat for user: {user} is: {chat}')
        if chat not in user.chat:
            logger.info(f'Chat {chat} not in user {user} chats')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
        return chat
    
    async def create(self, user, data:dict):
        # try to get chat with same name if so return error
        logger.info(f'Creating chat with data: {data} for user: {user}')
        chat = self.session.query(ChatModel).filter_by(name=data['name']).first()
        if chat:
            logger.info(f'Chat with name {data["name"]} already exists: {chat}')
            return 'Chat already exists'
        members = data["members_array"]
        members.append(user.id)
        members = list(set(members))
        logger.info(f'Chat members: {members}')
        for index,member in enumerate(members):
            members[index] = self.session.query(UserModel).filter_by(id=member).first()
            if not members[index]:
                return 'User not found'
        data['members_array'] = members
        chat = ChatModel(**data)
        self.session.add(chat)
        self.session.commit()
        logger.info(f'Chat created: {chat}')
        return {'chat': chat, 'members_array': members, "id": chat.id}
    
    async def toggle_pin(self, user, chat_id):
        user = self.session.query(UserModel).filter_by(id=user.id).first()
        chat = self.session.query(ChatModel).filter_by(id=chat_id).first()
        logger.info(f'Pinning chat {chat} for user {user}')
        if chat not in user.chat:
            logger.info(f'Chat {chat} not in user {user} chats')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
        pinned_chat = self.session.query(PinnedChatModel).filter_by(user=user.id).first()
        logger.info(f'Pinned chat: {pinned_chat}')
        if pinned_chat:
            if chat in pinned_chat.chats_array:
                pinned_chat.chats_array.remove(chat)
                self.session.commit()
                logger.info(f'Chat {chat} unpinned')
                return {'id': chat.id, 'pinned': False}
            else:
                pinned_chat.chats_array.append(chat)
                self.session.commit()
                logger.info(f'Chat {chat} pinned')
                return {'id': chat.id, 'pinned': True}

        else:
            pinned_chat = PinnedChatModel(user=user.id, chats_array=[chat])
            self.session.add(pinned_chat)
            self.session.commit()
            logger.info(f'Chat {chat} pinned')
            return {'id': chat.id, 'pinned': True}
        
    async def get_pinned_chats(self, user):
        user = self.session.query(UserModel).filter_by(id=user.id).first()
        pinned_chat = self.session.query(PinnedChatModel).filter_by(user=user.id).first()
        if pinned_chat:
            return pinned_chat.chats_array
        return []
        