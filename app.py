from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.user import router as user_router
from routers.chat import router as chat_router
from routers.message import router as message_router
import socketio

app = FastAPI()

from sockets.socketio import sio
socket_app = socketio.ASGIApp(sio, app)


app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
   


app.include_router(user_router)
app.include_router(chat_router)
app.include_router(message_router)
 
app.mount('/', socket_app)