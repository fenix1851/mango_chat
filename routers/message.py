from models.message import MessageModel
from models.user import UserModel
from repository.message import MessageRepository
from services.message import get_message_service
from jwt.get_current_user import get_current_user

from fastapi import APIRouter, Depends, Response, status

from exceptions.not_found import UserNotFoundException, ChatNotFoundException
from exceptions.jwt import InvalidTokenException, TokenExpiredException

router = APIRouter(prefix="/message", tags=["message"])

@router.get("/{chat_id}")
async def get_messages(chat_id: int,message_service=Depends(get_message_service), user: UserModel = Depends(get_current_user)):
    '''Get all messages of chat with id = chat_id. If user is not a member of chat, return 404'''
    try:
        return await message_service.get_messages(chat_id, user)
    except InvalidTokenException:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    except TokenExpiredException:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    except UserNotFoundException:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    except ChatNotFoundException:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    