from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .Crud import user_crud
from . Services import auth_service
from . import schemas,database,models
import os 
print(os.getcwd())

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
database.create_database()

@app.post("/auth/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    if user_crud.get_user_by_username(db, user.username) or user_crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Username or email already registered")
    if user.user_type not in [models.UserType.simple, models.UserType.photographer]:
        raise HTTPException(status_code=400, detail="Invalid user type")
    return user_crud.create_user(db, user)


@app.post("/auth/login", response_model=schemas.Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(database.get_db)):
    user = user_crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token_data = {"sub": str(user.id)}
    access_token = auth_service.create_access_token(token_data)
    return schemas.Token(access_token=access_token, token_type="bearer")

