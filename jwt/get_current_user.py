from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from datetime import datetime
from configs.vars import SALT
from database.connections import get_database_connection
from repository.user import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login", scheme_name="JWT")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    print("token: ", token)
    try:
        payload = jwt.decode(token, SALT, algorithms=["HS256"])
        if payload.get("exp") < datetime.timestamp(datetime.utcnow()):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except (jwt.JWTError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    print(payload.get("sub"))
    user = await UserRepository.get_by_phone(UserRepository(
        next(get_database_connection())), phone=payload.get("sub"))
    if not user:
        raise HTTPException(status_code=status.HTTP_410_GONE,
                            detail="User not found")
    return user
