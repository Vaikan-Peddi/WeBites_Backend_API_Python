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

class Signin(BaseModel):
    username: str
    password: str

class Signup(Signin):
    email: str
    mobile: str

class Token(BaseModel):
    access_token: str
    token_type: str