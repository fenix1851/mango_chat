from models.message import MessageModel
from models.user import UserModel
from models.message_type import MessageTypeModel
from models.chat import ChatModel
from repository.base import BaseRepository
from exceptions.not_found import ChatNotFoundException,\
    MessageTypeNotFoundException, MessageNotFoundException

from loguru import logger

class MessageRepository(BaseRepository):
    async def get_messages(self, chat_id, user):
        # check if user is member of chat
        user = self.session.query(UserModel).filter_by(id=user.id).first()
        chats = user.chat
        for chat in chats:
            if chat.id == chat_id:
                # return messages with likes_array (relationship)
                messages = messages = self.session.query(MessageModel).filter_by(\
                    chat_id=chat_id).order_by(MessageModel.created_at.desc()).all()
                results = []
                for message in messages:
                    message_dict = message.__dict__
                    likes = []
                    for like in message.likes_array:
                        likes.append({
                            'id': like.id,
                            'name': like.name,
                            'photo': like.photo
                        })
                    message_dict['likes_array'] = likes
                    results.append(message_dict)
                return results
        raise ChatNotFoundException(f"Chat with id {chat_id} was not found")

    async def create(self, user, message_data:dict):
        # check if user is member of chat
        user = self.session.query(UserModel).filter_by(id=user.id).first()
        chats = user.chat
        print(message_data)
        chat_id = message_data.get('chat_id', None)
        message_type = message_data.get('message_type', None)
        if chat_id is None:
            raise ChatNotFoundException("Chat not found")
        if message_type is None:
            raise MessageTypeNotFoundException("Message type not found")
        print('Message type', message_type)
        for chat in chats:
            if chat.id == chat_id:
                message_type = self.session.query(\
                    MessageTypeModel).filter_by(name=message_type).first()
                message_data['user_id'] = user.id
                message_data['message_type'] = message_type.id
                message = MessageModel(**message_data)
                self.session.add(message)
                self.session.commit()
                logger.info(f'Message created: {message.id}')
                return {'id': message.id, 'members_array': chat.members_array,\
                        'chat_id': chat.id, 'message_type': message_type.name\
                            , 'content': message.content, 'created_at': message.created_at}
        logger.info('Chat not found while creating message')
        raise ChatNotFoundException(f"Chat with id {chat_id} was not found")
    
    async def toggle_like(self, user, message_id):
        # check if user is member of chat
        user = self.session.query(UserModel).filter_by(id=user.id).first()
        message = self.session.query(MessageModel).filter_by(id=message_id).first()
        chat = self.session.query(ChatModel).filter_by(id=message.chat_id).first()
        logger.info(f'Toggling like for message: {message_id}')
        if message is None:
            logger.info('Message not found while toggling like')
            raise MessageNotFoundException(f"Message with id {message_id} was not found")
        if user in message.likes_array:
            logger.info(f'User {user.id} unliked message {message.id}')
            message.likes_array.remove(user)
        else:
            logger.info(f'User {user.id} unliked message {message.id}')
            message.likes_array.append(user)
        self.session.add(message)
        self.session.commit()
        return {'id': message.id, 'members_array': chat.members_array,\
                'chat_id': chat.id,'likes_array': message.likes_array}