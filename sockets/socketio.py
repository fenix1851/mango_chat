import socketio
from jwt import get_current_user
from fastapi import HTTPException
from socketio.exceptions import ConnectionRefusedError

from repository.user import UserRepository
from repository.chat import ChatRepository

from database.connections import get_database_connection

sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=["*"]
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
    except HTTPException as e:
        return False

    if current_user is None:
        return False

    print(f"Access token: {access_token}")
    print(f"Current user: {current_user.__dict__}")
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
        print('Client connected', sid)
        print('Joining to rooms...')
        chats = await ChatRepository.get_chats\
            (ChatRepository(next(get_database_connection())), current_user)
        for chat in chats:
            print('Joining to room: room_', chat.id)
            sio.enter_room(sid, "room_"+str(chat.id))
        print('Done!')
        print('Changing status to online...')
        await UserRepository.update_status\
            (UserRepository(next(get_database_connection())), \
             user=current_user, online=True, sid=sid)
        print('Done!')
        print('Saving session id...')
        await sio.save_session(sid, {'user': current_user, 'access_token': auth.get('access_token')})
        print('Done!')


@sio.on('disconnect')
async def test_disconnect(sid):
    print('Client disconnected', sid)
    print('Changing status to offline...')
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
    print("Checking if token expired...")
    session = await sio.get_session(sid)
    access_token = session.get('access_token')
    current_user = await \
        get_current_user.get_current_user(access_token)
    if not current_user:
        raise ConnectionRefusedError('authentication failed, token expired')    
    print('Validating data for creating chat...')
    # i don't know how to validate data from socketio right, \
    # so i'm just checking if the data is in the right format
    data_chat = data.get('chat')
    print('Chat data : ', data_chat)

    if data_chat:
        if type(data_chat['is_group']) is not bool or \
                type(data_chat['name']) is not str or \
                type(data_chat['members_array']) is not list:
            print('Wrong data format')
            return False
        print('Creating chat...')
        chat = await ChatRepository.create\
            (ChatRepository(next(get_database_connection())), \
                current_user, data_chat)
        if chat == 'Chat already exists':
            print('Chat already exists')
            return False
        print('Chat created: ', chat)
        print('Joining to room: room_', chat['id'])
        sio.enter_room(sid, "room_"+str(chat['id']))
        print('Done!')
        print('Sending chat to client...')
        for member in chat['members_array']:
            member = await UserRepository.get_by_id\
                (UserRepository(next(get_database_connection())), id=member.id, user=current_user)
            if member.online:
                print('Sending chat to client: ', member.sid)
                await sio.emit('chat_created', {'chat': chat['id']}, room=member.sid)
            else:
                print(f'User with sid: {member.id} is offline')
    else:
        print('Wrong data format')
        return False
        

        
