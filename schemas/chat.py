from pydantic import BaseModel
from typing import List, Optional


class ChatBaseSchema(BaseModel):
    name: str
    members: List[int]
    is_group: bool

class ChatUpdateSchema(BaseModel):
    name: Optional[str] = None
    members: Optional[List[int]] = None
    is_group: Optional[bool] = None
