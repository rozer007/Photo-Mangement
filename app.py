from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from schemas import *
from database import get_db
from models import User
from passlib.context import CryptContext
from .Crud import user_crud

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

from database import create_database
from models import User

create_database()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@app.post("/auth/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # if crud.user.get_user_by_username(db, user.username) or crud.user.get_user_by_email(db, user.email):
    #     raise HTTPException(status_code=400, detail="Username or email already registered")
    # if user.user_type not in [UserType.simple, UserType.photographer]:
    #     raise HTTPException(status_code=400, detail="Invalid user type")
    return user_crud.create_user(db, user)


@app.post("/auth/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(deps.get_db)):
    user = crud.user.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token_data = {"sub": str(user.id)}
    access_token = services.auth.create_access_token(token_data)
    return {"access_token": access_token, "token_type": "bearer"}

