from fastapi import FastAPI, Depends, APIRouter, status, Response
from models.user import UserModel
from schemas.user import UserBaseSchema, UserUpdateSchema
from services.user import get_user_service
from repository.user import UserRepository
from jwt.get_current_user import get_current_user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBaseSchema, user_service=Depends(get_user_service)):
    return await user_service.create(user)

@router.get("/me", status_code=status.HTTP_200_OK)
async def get_user_me(user: UserModel = Depends(get_current_user)):
    return user

@router.get('/{id}', status_code=status.HTTP_200_OK)
async def get_user_by_id(id: int, user_service=Depends(get_user_service), user=Depends(get_current_user)):
    return await user_service.get_by_id(id, user)

@router.post('/login', status_code=status.HTTP_200_OK)
async def login(response: Response,form_data: OAuth2PasswordRequestForm = Depends(), user_service=Depends(get_user_service)):
    return await user_service.login(form_data=form_data, response=response)

@router.post('/refresh', status_code=status.HTTP_200_OK)
async def refresh(refresh_token: str,response:Response, user_service=Depends(get_user_service)):
    return await user_service.refresh(refresh_token=refresh_token, response=response)

@router.patch('/{id}', status_code=status.HTTP_202_ACCEPTED)
async def patch_user(id: int, data: UserUpdateSchema, user_service=Depends(get_user_service), user=Depends(get_current_user)):
    return await user_service.patch(id, data, user)