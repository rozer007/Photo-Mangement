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
    
    follow = models.Follow(user_id=user_id, photographer_id=photographer_id)
    db.add(follow)
    db.commit()
    db.refresh(follow)
    return follow

def unfollow_photographer(db: Session, user_id: int, photographer_id: int):
    follow = db.query(models.Follow).filter_by(user_id=user_id, photographer_id=photographer_id).first()
    if follow:
        db.delete(follow)
        db.commit()
    return follow

def get_followers(db: Session, photographer_id: int):
    return db.query(models.Follow).filter_by(photographer_id=photographer_id).all()

def get_following(db: Session, user_id: int):
    return db.query(models.Follow).filter_by(user_id=user_id).all() 