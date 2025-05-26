from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import user_crud
from .. import models

def check_following(db:Session,user_id: int, photographer_id: int):
    exists_query= db.query(models.Follow).filter_by(user_id=user_id ,photographer_id = photographer_id).exists()
    user_exists = db.query(exists_query).scalar()
    return user_exists

def is_photographer(db: Session,photographer_id: int):
    try:
        photographer=user_crud.get_user_by_userid(db,photographer_id)
        return photographer.user_type == 'photographer'
    except :
        raise HTTPException(status_code=401, detail="No such photographer ID exists")

def is_simple_user(db: Session,user_id: int):
    simple=user_crud.get_user_by_userid(db,user_id)
    return simple.user_type == 'simple'

def follow_photographer(db: Session, user_id: int, photographer_id: int):
    if not is_photographer(db,photographer_id):
        raise HTTPException(status_code=401, detail="Please enter only photographer ID")
    
    if not is_simple_user(db,user_id):
        raise HTTPException(status_code=403, detail="Only simple user can follow/unfollow a photographer")
        
    exist=check_following(db,user_id,photographer_id)
    if exist:
        return None
    
    follow = models.Follow(user_id=user_id, photographer_id=photographer_id)
    db.add(follow)
    db.commit()
    db.refresh(follow)
    return follow

def unfollow_photographer(db: Session, user_id: int, photographer_id: int):

    if not is_photographer(db,photographer_id):
        raise HTTPException(status_code=401, detail="Please enter correct/existing photograher ID")
    
    if not is_simple_user(db,user_id):
        raise HTTPException(status_code=403, detail="Only Simple user can follow/unfollow a photographer")

    exist=check_following(db,user_id,photographer_id)
    if not exist:
        return None

    follow = db.query(models.Follow).filter_by(user_id=user_id, photographer_id=photographer_id).first()
    if follow:
        db.delete(follow)
        db.commit()
    return follow

def get_followers(db: Session,photographer_id: int):
    result=db.query(models.Follow).filter_by(photographer_id=photographer_id).all()
    if not len(result):
        raise HTTPException(status_code=401, detail="No followers")
    final=[]
    for res in result:
        id=res.id
        photographer_id=res.photographer_id
        user_id=res.user_id
        user_name=res.user.username
        final.append({"Id":id,"photographer_ID":photographer_id,"User_ID":user_id,'username':user_name})
    return final 

def get_following(db: Session, user_id: int):
    result= db.query(models.Follow).filter_by(user_id=user_id).all()
    if not len(result):
        raise HTTPException(status_code=401, detail="No followings")
    final=[]
    for res in result:
        id=res.id
        user_id=res.user_id
        photographer_id=res.photographer_id
        photographer_name=res.photographer.username
        final.append({"Id":id,"User_ID":user_id,"photographer_id":photographer_id,'photographer_name':photographer_name})
    return final 