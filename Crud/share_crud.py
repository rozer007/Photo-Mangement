from fastapi import HTTPException
from sqlalchemy.orm import Session
from .. import models
from ..Crud import photo_crud,follow_crud,user_crud
from datetime import datetime
import pytz

def create_share(db: Session, photo_id: int, from_user_id: int, to_user_id: int, expiry: datetime, link: str):
    photo=photo_crud.get_photo(db,photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="No such photo found")
    
    user=db.query(models.User).filter_by(id=to_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="No user with this id")
    
    if from_user_id!= photo.owner_id:
        user= user_crud.get_user_by_userid(db,from_user_id)

        if(user.user_type=='photographer'):
            raise HTTPException(status_code=403, detail="Not belongs to you")
            
        following=follow_crud.get_following(db,from_user_id)
        photographer_ids = [f['photographer_id'] for f in following]
        Photos=[]
        for pid in photographer_ids:
            Photos.extend(photo_crud.get_photos_by_owner(db, pid))

        photos_id=[p.id for p in Photos]

        if not photo_id in photos_id:
            raise HTTPException(status_code=403, detail="No such photo exist/Not following this photographer")

    share = models.Share(
        photo_id=photo_id,
        from_user_id=from_user_id,
        to_user_id=to_user_id,
        expiry=expiry,
        link=link
    )
    db.add(share)
    db.commit()
    db.refresh(share)
    return share

def get_share(db: Session, share_id: int):

    return db.query(models.Share).filter(models.Share.id == share_id).first()

def get_valid_share(db: Session, share_id: int):
    share = get_share(db, share_id)
    if share :

        india_tz = pytz.timezone('Asia/Kolkata')
        # Convert UTC expiry to India time
        expiry = share.expiry.astimezone(india_tz)

        india_time = datetime.now(india_tz)
        # print(expiry)
        # print(india_time)
        # print(expiry > india_time)


        if expiry > india_time:
            return share
    return None 

def delete_share(db: Session,share_id:int,current_user):
    share = get_share(db, share_id)

    if not share:
        raise HTTPException(status_code=404, detail="no such share photo found")
    
    if share.from_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not belongs to you")
    
    db.delete(share)
    db.commit()

    return share