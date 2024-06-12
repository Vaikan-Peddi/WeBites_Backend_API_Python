from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: str
    username: str
    mobile: str

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: int

    class Config:
        orm_mode: True

class UserResponse(UserInDB):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str