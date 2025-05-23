from fastapi import FastAPI, Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from . import database
from .Api import auth_api
from . import schemas,dependencies, database
from .Crud import follow_crud

app = FastAPI()

database.create_database()

app.include_router(auth_api.router, prefix="/auth", tags=["auth"]) #authentication

@app.post("/follow/{photographer_id}", response_model=schemas.FollowOut)
def follow_photographer(photographer_id: int, db: Session = Depends(database.get_db), current_user=Depends(dependencies.get_current_active_user)):
    followed = follow_crud.follow_photographer(db, current_user.id, photographer_id)
    if not followed:
        raise HTTPException(status_code=401, detail="Already following this photographer")
    return followed

@app.delete("/unfollow/{photographer_id}", response_model=schemas.FollowOut)
def unfollow_photographer(photographer_id: int, db: Session = Depends(database.get_db), current_user=Depends(dependencies.get_current_active_user)):
    return follow_crud.unfollow_photographer(db, current_user.id, photographer_id)

@app.get("/followers")
def get_photographer_follower(db:Session = Depends(database.get_db), current_user=Depends(dependencies.get_current_active_user)):
    if current_user.user_type == 'photographer':
        return follow_crud.get_followers(db,current_user.id)
    else:
        raise HTTPException(status_code=400, detail="Must be photographer")
    
@app.get("/followings")
def get_photographer_follower(db:Session = Depends(database.get_db), current_user=Depends(dependencies.get_current_active_user)):
    if current_user.user_type == 'simple':
        return follow_crud.get_following(db,current_user.id)
    else:
        raise HTTPException(status_code=400, detail="Must be simple user")