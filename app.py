import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.user import router as user_router

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
    
sio = socketio.AsyncServer(
  async_mode='asgi',
  cors_allowed_origins=["*"]
  )
socket_app = socketio.ASGIApp(sio, app)

app.include_router(user_router)

async def check_session(sid):
    session = await sio.get_session(sid)
    if not session or 'token' not in session:
        return False
    token = session['token']
    if token == 'test_token':
        return True
    else:
        print('Not Connected!')
        await sio.emit('connect', room=sid, data={'message': 'Not Connected!'})
        return False    

@sio.on('disconnect')
async def test_disconnect(sid):
  print('Client disconnected')

@sio.on('connect')
async def connection(sid, environ, auth):
    return await sio.emit('connect', room=sid, data={'message': 'Connected!'})


@sio.on('join')
async def on_join(sid,data):
    room = data['room']
    print(room)
    # join room async
    sio.enter_room(sid, room)
    return await sio.emit('user_join', skip_sid=sid, data='Welcome to room '+room, room=room)


@sio.event
async def message_to_room(sid, data):
    room = data['room']
    message = data['message']
    if(room == ''):
        print(f'no room message {message}')
        await sio.emit('message_to_room', {'message': message}, skip_sid=sid, sid=sid)
    else:
        print(f'room {room} message {message}')
        return await sio.emit('message_to_room', {'message': message}, room=room, skip_sid=sid)

app.mount('/', socket_app)