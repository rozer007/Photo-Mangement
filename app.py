from fastapi import FastAPI
from passlib.context import CryptContext
from . import database
from .Api import auth_api

app = FastAPI()

database.create_database()

app.include_router(auth_api.router, prefix="/auth", tags=["auth"]) #authentication
