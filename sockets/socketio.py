import socketio
from jwt import get_current_user
from fastapi import HTTPException
from socketio.exceptions import ConnectionRefusedError

from repository.user import UserRepository
from repository.chat import ChatRepository
from repository.message import MessageRepository

from database.connections import get_database_connection

from exceptions.not_found import UserNotFoundException, ChatNotFoundException
from exceptions.jwt import InvalidTokenException, TokenExpiredException
from exceptions.validation import ChatAlreadyExistsException

from loguru import logger

sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=["*"],
    namespaces=['/ws']
    )


# helper for getting the current user
# -----------------------------------
async def authenticate(sid, environ):
    if (environ is None):
        return False
    access_token = environ.get('HTTP_AUTH', None)
    if access_token is None:
        return False

    try:
        current_user = await \
            get_current_user.get_current_user(access_token)
    except (InvalidTokenException, TokenExpiredException, UserNotFoundException):
        return False

    if current_user is None:
        return False

    logger.info(f'User authenticated through socket: {current_user.id}')
    return {'sid': sid, 'user': current_user, 'access_token': access_token}

# socketio events
# ---------------

# connection events
@sio.on('connect')
async def connection(sid, environ, *args, **kwargs):
    print('environ', environ)
    if environ is None:
        raise ConnectionRefusedError(
            'authentication failed, no token provided')
    auth = await authenticate(sid, environ)
    if not auth:
        raise ConnectionRefusedError('authentication failed')
    else:
        current_user = auth.get('user')
        logger.info(f'Joining room: {current_user.id}')
        chats = await ChatRepository.get_chats\
            (ChatRepository(next(get_database_connection())), current_user)
        for chat in chats:
            logger.info(f'Joining room: {chat.id}')
            sio.enter_room(sid, "room_"+str(chat.id))
        logger.info(f'User {current_user.id} joined all rooms')
        await UserRepository.update_status\
            (UserRepository(next(get_database_connection())), \
            user=current_user, online=True, sid=sid)
        logger.info(f'User {current_user.id} status updated to online, saving session...')
        await sio.save_session(sid, {'user': current_user, 'access_token': auth.get('access_token')})
        logger.info(f'User {current_user.id} session saved')


@sio.on('disconnect')
async def test_disconnect(sid):
    session = await sio.get_session(sid)
    user = session.get('user')
    await UserRepository.update_status\
        (UserRepository(next(get_database_connection())), \
         user=user, online=False, sid=None)


# chat events
# -----------
@sio.on('create_chat')
async def create_chat(sid, data):
    # check if token expired
    logger.info(f"{sid}trying to create chat")
    session = await sio.get_session(sid)
    access_token = session.get('access_token')
    current_user = await \
        get_current_user.get_current_user(access_token)
    if not current_user:
        logger.info(f"{sid}token expired")
        raise ConnectionRefusedError('authentication failed, token expired')    
    # i don't know how to validate data from socketio right, \
    # so i'm just checking if the data is in the right format
    data_chat = data.get('chat')

    if data_chat:
        if type(data_chat['is_group']) is not bool or \
                type(data_chat['name']) is not str or \
                type(data_chat['members_array']) is not list:
            logger.info(f"{current_user.id}wrong data format for chat")
            return False
        try:
            chat = await ChatRepository.create\
                (ChatRepository(next(get_database_connection())), \
                    current_user, data_chat)
        except (UserNotFoundException, ChatNotFoundException):
            logger.info(f"{current_user.id}user or chat not found")
            return False
        
        logger.info(f"{current_user.id}chat created")
        sio.enter_room(sid, "room_"+str(chat['id']))
        logger.info(f"{current_user.id}joining to room: room_{chat['id']} done")
        for member in chat['members_array']:
            member = await UserRepository.get_by_id\
                (UserRepository(next(get_database_connection())), id=member.id, user=current_user)
            if(not member):
                logger.info(f"{current_user.id}user not found")
                return False
            if member.online:
                logger.info(f"{current_user.id}user online, notifying")
                await sio.emit('chat_created', {'chat': chat['id']}, room=member.sid)
                logger.info(f"{current_user.id}notified")
            else:
                logger.info(f"{current_user.id}user offline")
        logger.info(f"{current_user.id}chat created, users notified")
    else:
        print('Wrong data format')
        logger.info(f"{current_user.id}wrong data format")
        return False

@sio.on('toggle_chat_pin')
async def toggle_chat_pin(sid, data):
    # check if token expired
    session = await sio.get_session(sid)
    access_token = session.get('access_token')
    current_user = await \
        get_current_user.get_current_user(access_token)
    if not current_user:
        raise ConnectionRefusedError('authentication failed, token expired')    
    # i don't know how to validate data from socketio right, \
    # so i'm just checking if the data is in the right format
    data_chat = data.get('chat')
    print('Chat data : ', data_chat)

    if data_chat:
        if type(data_chat['id']) is not int:
            logger.info(f"{current_user.id}wrong data format for pinning chat")
            return False
        print('Toggling chat pin...')
        try:
            chat = await ChatRepository.toggle_pin\
                (ChatRepository(next(get_database_connection())), \
                    current_user, data_chat['id'])
        except (UserNotFoundException, ChatNotFoundException):
            print('User or chat not found')
            return False
        
        # send caht pinned event to current user
        if current_user.online:
            if chat['pinned']:
                await sio.emit('chat_pinned', {'chat': chat['id']}, room=current_user.sid)
            if not chat['pinned']:
                await sio.emit('chat_unpinned', {'chat': chat['id']}, room=current_user.sid)
    else:
        print('Wrong data format')
        return False

# message events
# --------------
@sio.on('send_message')
async def send_message(sid,data):
    # check if token expired
    session = await sio.get_session(sid)
    access_token = session.get('access_token')
    current_user = await \
        get_current_user.get_current_user(access_token)
    if not current_user:
        raise ConnectionRefusedError('authentication failed, token expired')    
    # i don't know how to validate data from socketio right, \
    # so i'm just checking if the data is in the right format
    data_message = data.get('message')
    logger.info(f"{current_user.id}trying to send message")

    if data_message:
        if type(data_message['chat_id']) is not int or \
                type(data_message['content']) is not str or\
                    type(data_message['message_type']) is not str:
            print('Wrong data format')
            logger.info(f"{current_user.id}wrong data format for sending message")
            return False
        try:
            logger.info(f"{current_user.id}sending message...")
            message = await MessageRepository.create\
                (MessageRepository(next(get_database_connection())), \
                    user=current_user, message_data=data_message)
        except Exception as e:
            logger.info(f"{current_user.id}error while sending message")
            return False
        message = message
    
        print('Message sent: ', message)
        logger.info(f"{current_user.id}message sent")
        print('Sending message to client...')
        logger.info(f"{current_user.id}sending message to client")
        for member in message['members_array']:
            if member.id == current_user.id:
                continue
            member = await UserRepository.get_by_id\
                (UserRepository(next(get_database_connection())), id=member.id, user=current_user)
            if member.online:
                print('Sending message to client: ', member.sid)
                logger.info(f"{current_user.id}sending message to client: {member.sid}")
                await sio.emit('new_message', {'content':message['content'],\
                                               'message_type':message['message_type'],\
                                                  "chat":message['chat_id']},\
                                                      room="room_"+str(message['chat_id']),
                                                        skip_sid=sid)
            else:
                logger.info(f"{current_user.id}user offline")
                print(f'User with sid: {member.id} is offline')
    else:
        logger.info(f"{current_user.id}wrong data format")
        print('Wrong data format')
        return False    
        
@sio.on('toggle_like_message')
async def like_message(sid,data):
    print("Checking if token expired...")
    session = await sio.get_session(sid)
    access_token = session.get('access_token')
    current_user = await \
        get_current_user.get_current_user(access_token)
    if not current_user:
        raise ConnectionRefusedError('authentication failed, token expired')
    print('Validating data for liking message...')
    # i don't know how to validate data from socketio right, \
    # so i'm just checking if the data is in the right format
    data_message = data.get('message')
    logger.info(f"{current_user.id}trying to like message")
    
    if data_message:
        if type(data_message['id']) is not int:
            print('Wrong data format')
            logger.info(f"{current_user.id}wrong data format for liking message")
            return False
        print('Toggle like to message...')
        try:
            message = await MessageRepository.toggle_like\
                (MessageRepository(next(get_database_connection())), \
                    user=current_user, message_id=data_message['id'])
        except Exception as e:
            print('Error while toogle like on message: ', e)
            logger.info(f"{current_user.id}error while liking message")
            return False
        message = message
        print('Message liked: ', message)
        print('Sending message to client...')
        logger.info(f"{current_user.id}sending message to client")
        for member in message['members_array']:
            if member.id == current_user.id:
                continue
            member = await UserRepository.get_by_id\
                (UserRepository(next(get_database_connection())), \
                 id=member.id, user=current_user)
            if member.online:
                logger.info(f"{current_user.id}sending message to client: {member.sid}")
                print('Sending message to client: ', member.sid)
                await sio.emit('message_liked', {'message_id':message['id']},\
                                                      room="room_"+str(message['chat_id']),
                                                        skip_sid=sid)
            else:
                logger.info(f"{current_user.id}user offline")
                print(f'User with sid: {member.id} is offline')