from pydantic import BaseModel, EmailStr, field_validator, constr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    username: str
    mobile: constr(pattern=r'^\+91\d{10}$') # type: ignore

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: int

    college_id: int | None = None

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

class College(BaseModel):
    name: str
    state: str

class CollegeInDB(BaseModel):
    id: int

    class Config:
        orm_mode: True

class CollegeResponse(CollegeInDB):
    pass