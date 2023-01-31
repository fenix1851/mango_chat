from models.user import UserModel
from fastapi import Response, HTTPException, Depends, status, Cookie  
from repository.base import BaseRepository
from schemas.user import UserBaseSchema, UserUpdateSchema
from passlib.hash import pbkdf2_sha256
from configs.vars import SALT
from jose import jwt
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta

pwd_context = pbkdf2_sha256
pwd_context.using(salt=SALT.encode('utf-8'))

class UserRepository(BaseRepository):
    async def create(self, data: UserBaseSchema):
        check_user = self.get_by_phone(data.phone)
        print(check_user)
        if check_user:
            raise HTTPException(status_code=403, detail="User with this phone already exists")
        user = data.__dict__
        user["hashed_password"] = pwd_context.hash(data.password)
        #remove password key from user
        del user['password']
        user = UserModel(**user)
        self.session.add(user)
        self.session.commit()
        return user
    
    def get_by_id(self, id: int, user):
        user = self.session.query(UserModel).filter(UserModel.id == id).first()
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
    def login(self, response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
        user = self.get_by_login(form_data.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if not self.verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

        # create access and refresh tokens
        access_token = self.create_access_token(
            data={"sub": user.phone})
        refresh_token = self.create_refresh_token(
            data={"sub": user.phone})
        user.refresh_token = refresh_token
        self.session.commit()
        response.set_cookie(key="refresh_token", value=refresh_token)
        return {"access_token": access_token, "token_type": "bearer"}

    def refresh(self, response: Response, refresh_token: str = Cookie(None)):
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token not found")
        user = self.session.query(UserModel).filter(
            UserModel.refresh_token == refresh_token).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token not found")
        access_token = self.create_access_token(
            data={"sub": user.phone})
        response.set_cookie(key="refresh_token", value=refresh_token)
        return {"access_token": access_token, "token_type": "bearer"}


    def patch_user(self, id: int, data: UserUpdateSchema, user):
        user = self.session.query(UserModel).filter(UserModel.id == id).first()
        if user.id == user.id:
            for key, value in data.__dict__.items():
                setattr(user, key, value)
            self.session.commit()
            return user
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can't change other users data")

    # helpers
    # -------
    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=30)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SALT, algorithm="HS256")
        return encoded_jwt

    def create_refresh_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SALT, algorithm="HS256")
        return encoded_jwt

    def get_hashed_password(self, password: str) -> str:
        return pwd_context.hash(password)
    
    def verify_password(self, password: str, hashed_pass: str) -> bool:
        return pwd_context.verify(password, hashed_pass)
    
    async def get_by_name(self, name: str):
        return await self.session.query(UserModel).filter(UserModel.name == name).first()
    
    def get_by_phone(self, phone: str):
        print(self.session.query(UserModel).first().__dict__)
        return self.session.query(UserModel).filter(UserModel.phone == phone).first().__dict__
    
    
