from fastapi import FastAPI, Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from . import database
from .Api import auth_api,follow_api,photo_api,share_api,review_api
from . import schemas,dependencies, database
from .Crud import follow_crud
from . import models

app = FastAPI()

database.create_database()

app.include_router(auth_api.router, prefix="/auth", tags=["Authentication"]) #authentication
app.include_router(follow_api.router, prefix="/follows", tags=["Follows"]) #Follows
app.include_router(photo_api.router, prefix="/photos", tags=["Photos"]) #Photos
app.include_router(share_api.router, prefix="/sharing", tags=["Sharing"]) #Share Photos
app.include_router(review_api.router, prefix="/reviews", tags=["Reviews"]) #reviews Photos and photographer



    