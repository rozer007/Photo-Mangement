from pydantic import BaseModel, EmailStr, validator 
from fastapi import UploadFile
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str
    user_type: str

    @validator('user_type')
    def validate_user_type(cls, v):
        if v!= "simple" and v!="photographer":
            raise ValueError('User_type must be photographer or simple user')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v
    
    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        return v
    
class UserOut(UserBase):
    id: int
    username :str
    class Config:
        from_attribute = True
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class FollowOut(BaseModel):
    id: int
    user_id: int
    photographer_id: int
    class Config:
        from_attribute = True

class PhotoBase(BaseModel):
    description: Optional[str]
    tags: Optional[str]

class PhotoCreate(PhotoBase):
    file_size:float
    pass

class PhotoOut(PhotoCreate):
    id: int
    file_path: str
    owner_id: int
    created_at: datetime

    class Config:
        from_attribute = True



