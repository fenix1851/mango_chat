from fastapi import APIRouter, Depends, status, Response
from models.chat import ChatModel
from models.user import UserModel
from repository.chat import ChatRepository
from schemas.chat import ChatBaseSchema, ChatUpdateSchema
from services.chat import get_chat_service
from jwt.get_current_user import get_current_user

router = APIRouter(prefix="/chat", tags=["chat"])

@router.get("/", status_code=status.HTTP_200_OK)
async def get_chats(user: UserModel = Depends(get_current_user), chat_service=Depends(get_chat_service)):
    '''Get all chats of user with id = user.id'''
    return await chat_service.get_chats(user)


@router.get("/pinned", status_code=status.HTTP_200_OK)
async def get_pinned_chats(user: UserModel = Depends(get_current_user), chat_service=Depends(get_chat_service)):
    '''Get all pinned chats of user with id = user.id'''
    return await chat_service.get_pinned_chats(user)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_chat(id: int, user: UserModel = Depends(get_current_user), chat_service=Depends(get_chat_service)):
    '''Get chat with id = id, if user is not a member of chat, return 404'''
    return await chat_service.get_by_id(id, user)
