from models.user import UserModel
from fastapi import Response, Depends, status, Cookie, UploadFile  
from repository.base import BaseRepository
from schemas.user import UserBaseSchema, UserUpdateSchema
from passlib.hash import pbkdf2_sha256
from configs.vars import SALT
from jose import jwt
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import base64
import binascii
import uuid
import os
from PIL import Image
from io import BytesIO
from loguru import logger
from exceptions.not_found import UserNotFoundException, RefreshTokenNotFoundException
from exceptions.validation import UserWithPhoneAlreadyExistsException,\
    NotValidPhotoException, IncorrectPasswordException, AccessDeniedException


pwd_context = pbkdf2_sha256
pwd_context.using(salt=SALT.encode('utf-8'))

class UserRepository(BaseRepository):
    async def create(self, data: UserBaseSchema):
        logger.info(f'Creating user with data: {data}')
        check_user = await self.get_by_phone(data.phone)
        if check_user:
            logger.info(f'User with phone {data.phone} already exists: {check_user}')
            raise UserWithPhoneAlreadyExistsException\
                (f"User with phone {data.phone} already exists")
        user = data.__dict__
        # check if photo is base64
        if not self.is_valid_base64(user['photo']):
            logger.info(f'Photo is not valid base64: {user["photo"]}')
            raise NotValidPhotoException\
                (f"Photo is not valid base64")
        else:
            decoded_photo = base64.b64decode(user['photo'])
            photo_uuid = uuid.uuid4()
            os.mkdir(f'static/{photo_uuid}')
            with open(f'static/{photo_uuid}/original.jpg', 'wb') as f:
                f.write(decoded_photo)
            # get path to photo by os.path
            path = f'static/{photo_uuid}/original.jpg'
            logger.info(f'Path to photo: {path}')
            output_path = os.path.join(os.getcwd(), f'static/{photo_uuid}/')
            # resize and save photo in 50x50, 100x100, 400x400
            await self.resize_and_save(path, output_path, (50, 50))
            await self.resize_and_save(path, output_path, (100, 100))
            await self.resize_and_save(path, output_path, (400, 400))
            # set photo_uuid to user
            user['photo'] = str(photo_uuid)

        # hash password
        user["hashed_password"] = pwd_context.hash(data.password)
        #remove password key from user
        del user['password']
        user = UserModel(**user)
        self.session.add(user)
        self.session.commit()
        logger.info(f'User created: {user}')
        return user
    
    async def get_by_id(self, id: int, user):
        user = self.session.query(UserModel).filter(UserModel.id == id).first()
        if not user:
            raise UserNotFoundException\
                (f"User not found")
        if user.id == user.id:
            return user
        else:
            # return user without password, refresh_token and phone
            user = self.session.query(UserModel).filter(UserModel.id == id).first()
            user = user.__dict__
            del user['hashed_password']
            del user['refresh_token']
            del user['phone']
            return user
    

    # refresh and login
    # ----------------
    async def login(self, response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
        user = await self.get_by_phone(form_data.username)
        if not user:
            raise UserNotFoundException\
                (f"User not found")
        if not self.verify_password(form_data.password, user.hashed_password):
            raise IncorrectPasswordException\
                (f"Incorrect password")
        # create access and refresh tokens
        access_token = await self.create_access_token(
            data={"sub": user.phone})
        refresh_token = await self.create_refresh_token(
            data={"sub": user.phone})
        user.refresh_token = refresh_token
        self.session.commit()
        response.set_cookie(key="refresh_token", value=refresh_token)
        logger.info(f'User logged in: {user}')
        return {"access_token": access_token, "token_type": "bearer"}

    async def refresh(self, response: Response, refresh_token: str = Cookie(None)):
        if not refresh_token:
            raise RefreshTokenNotFoundException\
                (f"Refresh token not found")
        user = self.session.query(UserModel).filter(
            UserModel.refresh_token == refresh_token).first()
        if not user:
            raise RefreshTokenNotFoundException\
                (f"Refresh token not found")
        access_token = await self.create_access_token(
            data={"sub": user.phone})
        response.set_cookie(key="refresh_token", value=refresh_token)
        logger.info(f'User refreshed: {user}')
        return {"access_token": access_token, "token_type": "bearer"}


    async def patch(self, id: int, data: UserUpdateSchema, user):
        user_in_db = self.session.query(UserModel).filter(UserModel.id == id).first()
        data = data.dict(exclude_unset=True)
        # exclude_unset = True
        if user_in_db.id == user.id:
            for key, value in data.items():
                if key == 'photo':
                    if not self.is_valid_base64(value):
                        raise NotValidPhotoException\
                            (f"Photo is not valid base64")
                    else:
                        decoded_photo = base64.b64decode(value)
                        photo_uuid = uuid.uuid4()
                        os.mkdir(f'static/{photo_uuid}')
                        with open(f'static/{photo_uuid}/original.jpg', 'wb') as f:
                            f.write(decoded_photo)
                        # get path to photo by os.path
                        path = f'static/{photo_uuid}/original.jpg'
                        output_path = os.path.join(os.getcwd(), f'static/{photo_uuid}/')
                        # resize and save photo in 50x50, 100x100, 400x400
                        await self.resize_and_save(path, output_path, (50, 50))
                        await self.resize_and_save(path, output_path, (100, 100))
                        await self.resize_and_save(path, output_path, (400, 400))

                        setattr(user_in_db, key, str(photo_uuid))
                else:
                    setattr(user_in_db, key, value)
            self.session.commit()
            logger.info(f'User updated: {user_in_db}')
            return user_in_db
        else:
            logger.info(f'User tried to change other users data: {user}')
            raise AccessDeniedException\
                (f"Access denied")

    # update for socket
    # -----------------
    async def update_status(self, user, online: bool, sid: str):
        user = self.session.query(UserModel).filter(UserModel.id == user.id).first()
        if online:
            logger.info(f'User {user} is now online, sid: {sid}')
        else:
            logger.info(f'User {user} is now offline')
        user.online = online
        user.sid = sid
        self.session.commit()
        return user

    # helpers
    # -------
    async def photo_to_base64(self, image_data: bytes):
        logger.info(f'Someone tried to convert photo to base64')
        return base64.b64encode(image_data)
    
    async def resize_and_save(self, path_to_image: str, output_image_path: str, size:list) -> None:
        original_image = Image.open(path_to_image)
        width, height = original_image.size
        print(f"The original image size is {width} wide x {height} tall")
        resized_image = original_image.resize(size)
        width, height = resized_image.size
        print(f"The resized image size is {width} wide x {height} tall")
        resized_image.save(output_image_path+f'{width}x{height}.webp')

    async def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=30)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SALT, algorithm="HS256")
        return encoded_jwt

    async def create_refresh_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SALT, algorithm="HS256")
        return encoded_jwt

    async def get_hashed_password(self, password: str) -> str:
        return pwd_context.hash(password)
    
    def verify_password(self, password: str, hashed_pass: str) -> bool:
        return pwd_context.verify(password, hashed_pass)
    
    async def get_by_name(self, name: str):
        return await self.session.query(UserModel).filter(UserModel.name == name).first()
    
    async def get_by_phone(self, phone: str):
        return self.session.query(UserModel).filter(UserModel.phone == phone).first()

    def is_valid_base64(self,string:str) -> bool:
        try:
            base64.b64decode(string)
            return True
        except (TypeError, binascii.Error):
            return False
