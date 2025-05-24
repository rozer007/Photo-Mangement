from sqlalchemy.orm import Session
from .. import models

def check_following(db:Session,user_id: int, photographer_id: int):
    exists_query= db.query(models.Follow).filter_by(user_id=user_id ,photographer_id = photographer_id).exists()
    user_exists = db.query(exists_query).scalar()
    return user_exists

def follow_photographer(db: Session, user_id: int, photographer_id: int):
    exist=check_following(db,user_id,photographer_id)
    if exist:
        return None
    # check whether the photographer_id belongs to photographer and same for user
    follow = models.Follow(user_id=user_id, photographer_id=photographer_id)
    db.add(follow)
    db.commit()
    db.refresh(follow)
    return follow

def unfollow_photographer(db: Session, user_id: int, photographer_id: int):
    exist=check_following(db,user_id,photographer_id)
    if not exist:
        return None
     # check weather the photographer_id belongs to photographer and same for user
    follow = db.query(models.Follow).filter_by(user_id=user_id, photographer_id=photographer_id).first()
    if follow:
        db.delete(follow)
        db.commit()
    return follow

def get_followers(db: Session,photographer_id: int):
    result=db.query(models.Follow).filter_by(photographer_id=photographer_id).all()
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
    final=[]
    for res in result:
        id=res.id
        user_id=res.user_id
        photographer_id=res.photographer_id
        photographer_name=res.photographer.username
        final.append({"Id":id,"User_ID":user_id,"photographer_id":photographer_id,'photographer_name':photographer_name})
    return final 