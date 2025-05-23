from pydantic import BaseModel, EmailStr, validator # type: ignore
from typing import Optional
from datetime import datetime
# Hello

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str
    user_type: str

    @validator('user_type')
    def validate_user_type(cls, v):
        if v!= "simple" or v!="photographer":
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
    
# class UserUpdate(BaseModel):
#     email: Optional[EmailStr] = None
#     username: Optional[str] = None
    
#     @validator('username')
#     def validate_username(cls, v):
#         if v is not None and len(v) < 3:
#             raise ValueError('Username must be at least 3 characters long')
#         return v

# class UserPasswordUpdate(BaseModel):
#     new_password: str
    
#     @validator('new_password')
#     def validate_password(cls, v):
#         if len(v) < 6:
#             raise ValueError('Password must be at least 6 characters long')
#         return v
