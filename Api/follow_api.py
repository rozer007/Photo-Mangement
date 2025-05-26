from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..Crud import follow_crud
from .. import dependencies
from .. import schemas,database


router =APIRouter()

@router.post("/follow/{photographer_id}", response_model=schemas.FollowOut)
def follow_photographer(photographer_id: int, db: Session = Depends(database.get_db), current_user=Depends(dependencies.get_current_active_user)):
    followed = follow_crud.follow_photographer(db, current_user.id, photographer_id)
    if not followed:
        raise HTTPException(status_code=401, detail="Already following this photographer")
    return followed

@router.delete("/unfollow/{photographer_id}", response_model=schemas.FollowOut)
def unfollow_photographer(photographer_id: int, db: Session = Depends(database.get_db), current_user=Depends(dependencies.get_current_active_user)):
    un_followed = follow_crud.unfollow_photographer(db, current_user.id, photographer_id)
    if not un_followed:
            raise HTTPException(status_code=401, detail="Can't unfollow as you are not following this photographer")
    return un_followed

@router.get("/followers")
def get_photographer_follower(db:Session = Depends(database.get_db), current_user=Depends(dependencies.get_current_active_user)):
    if current_user.user_type == 'photographer':
        return follow_crud.get_followers(db,current_user.id)
    else:
        raise HTTPException(status_code=403, detail="Must be photographer")
    
@router.get("/followings")
def get_followings(db:Session = Depends(database.get_db), current_user=Depends(dependencies.get_current_active_user)):
    if current_user.user_type == 'simple':
        return follow_crud.get_following(db,current_user.id)
    else:
        raise HTTPException(status_code=403, detail="Must be simple user")