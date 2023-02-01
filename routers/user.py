from fastapi import FastAPI, Depends, APIRouter, status, Response, File, UploadFile
from models.user import UserModel
from schemas.user import UserBaseSchema, UserUpdateSchema
from services.user import get_user_service
from repository.user import UserRepository
from jwt.get_current_user import get_current_user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBaseSchema, user_service=Depends(get_user_service)):
    '''Create user, return 201. Password is hashed with bcrypt. Photo is saved in static/{user.photo}/original.jpg. '''
    return await user_service.create(user)

@router.get("/me", status_code=status.HTTP_200_OK)
async def get_user_me(user: UserModel = Depends(get_current_user)):
    '''Get user with id = user.id'''
    return user

@router.get('/{id}', status_code=status.HTTP_200_OK)
async def get_user_by_id(id: int, user_service=Depends(get_user_service), user=Depends(get_current_user)):
    '''Get info about user with id = id. If user trying to get your own info, return full info. Else return data without password, refresh_token and phone'''
    return await user_service.get_by_id(id, user)

@router.post('/login', status_code=status.HTTP_200_OK)
async def login(response: Response,form_data: OAuth2PasswordRequestForm = Depends(), user_service=Depends(get_user_service)):
    '''Login with fastapi.security.OAuth2PasswordRequestForm. Return 200 and set cookies with access_token and refresh_token.'''
    return await user_service.login(form_data=form_data, response=response)

@router.post('/refresh', status_code=status.HTTP_200_OK)
async def refresh(response:Response, user_service=Depends(get_user_service), user=Depends(get_current_user)):
    '''Refresh access_token with refresh_token. Return 200, string with access_token and set cookies with access_token and refresh_token.'''
    return await user_service.refresh(refresh_token=user.refresh_token, response=response)

@router.patch('/{id}', status_code=status.HTTP_202_ACCEPTED)
async def patch_user(id: int, data: UserUpdateSchema, user_service=Depends(get_user_service), user=Depends(get_current_user)):
    '''Update user with id = id. All fields are optional.'''
    return await user_service.patch(id, data, user)

@router.post("/photo_to_base64", status_code=status.HTTP_200_OK)
async def photo_to_base64(image: UploadFile = File(), user_service=Depends(get_user_service)):
    '''Convert photo to base64. Return 200 and string with base64.'''
    return await user_service.photo_to_base64(image.file.read())