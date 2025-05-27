from pydantic import BaseModel, EmailStr, validator 
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


class ShareOut(BaseModel):
    id: int
    photo_id: int
    from_user_id: int
    to_user_id: int
    expiry: datetime
    link: str
    class Config:
        from_attribute = True

class ReviewCreate_Photo(BaseModel):
    photo_id: int
    rating: int

    @validator('rating')
    def validate_rating(cls, v):
        if v<=0 or v>10:
            raise ValueError('Rating must be between 1-10')
        return v
    
    comment: Optional[str]

class ReviewCreate_Photographer(BaseModel):

    photographer_id:int
    rating: float

    @validator('rating')
    def validate_rating(cls, v):
        if v<=0 or v>10:
            raise ValueError('Rating must be between 1-10')
        return v
    comment: Optional[str]

class ReviewOut(BaseModel):
    id: int
    user_id: int
    photo_id: Optional[int]
    photographer_id: Optional[int]
    rating: float
    comment: Optional[str]
    class Config:
        from_attribute = True



