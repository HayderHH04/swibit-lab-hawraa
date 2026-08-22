from pydantic import BaseModel, ConfigDict
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    is_admin: Optional[bool] = False


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email:Optional[str] = None
    password: Optional[str] = None


class UserResponse(BaseModel):
    username: str
    id: int
    is_admin: bool
    

    model_config = ConfigDict(from_attributes=True)