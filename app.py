from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from starlette.staticfiles import StaticFiles

from loguru import logger

from routers.user import router as user_router
from routers.chat import router as chat_router
from routers.message import router as message_router
import socketio

from sockets.socketio import sio

app = FastAPI()
socket_app = socketio.ASGIApp(sio, app)


@app.on_event("startup")
def startup_event():
    logger.add(
        "./assets/logs/latest.log", rotation="200 KB", enqueue=True, level="INFO"
    )
    logger.info("App started")

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
 
app.mount('/ws', socket_app)
app.mount("/static", StaticFiles(directory="static"), name="static")