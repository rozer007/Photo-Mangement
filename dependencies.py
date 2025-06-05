
from fastapi import Depends, HTTPException,status,Cookie,Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import database,models
from .Services import auth_service
from .Crud import user_crud
from typing import Optional


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user_oauth2_scheme(token:str=Depends(oauth2_scheme),db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if token is None:
         raise credentials_exception

    user_id: int = auth_service.verify_token(token)

    if user_id is None:
            raise credentials_exception
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_user(request:Request,db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    access_token = request.cookies.get("access_token")
    if access_token is None:
         raise credentials_exception

    user_id: int = auth_service.verify_token(access_token)

    if user_id is None:
            raise credentials_exception
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_current_photographer(current_user: models.User = Depends(get_current_active_user)):
    if current_user.user_type != "photographer":
        raise HTTPException(status_code=403, detail="Not a photographer")
    return current_user 
