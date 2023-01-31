from pydantic import BaseModel
from typing import List, Optional


class UserBaseSchema(BaseModel):
    password: str
    phone: str
    photo: str

class UserLoginSchema(BaseModel):
    phone: str
    password: str

class UserUpdateSchema(BaseModel):
    name: Optional[str] = None 
    phone: Optional[str] = None
    password: Optional[str] = None
    photo: Optional[str] = None
    description: Optional[str] = None

