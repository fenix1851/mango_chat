from models.message import MessageModel
from models.user import UserModel
from repository.message import MessageRepository
from services.message import get_message_service
from jwt.get_current_user import get_current_user

from fastapi import APIRouter, Depends, HTTPException, status


router = APIRouter(prefix="/message", tags=["message"])

@router.get("/{chat_id}")
async def get_messages(chat_id: int,message_service=Depends(get_message_service), user: UserModel = Depends(get_current_user)):
    return await message_service.get_messages(chat_id, user)
    