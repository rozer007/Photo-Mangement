from sqlalchemy.orm import Session
from .. import models, schemas

def create_review_photo(db: Session, review: schemas.ReviewOut,current_user):
    db_review = models.Review(
        user_id=current_user.id,
        photo_id=review.photo_id,
        rating=review.rating,
        comment=review.comment
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def create_review_photographer(db: Session, review: schemas.ReviewOut,current_user):
    
    db_review = models.Review(
        user_id=current_user.id,
        photographer_id=review.photographer_id,
        rating=review.rating,
        comment=review.comment
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def check_reviews_for_photo(db: Session, photo_id: int,user_id:int):
    return db.query(models.Review).filter(models.Review.photo_id == photo_id,models.Review.user_id==user_id).all() 

def check_reviews_for_photographer(db: Session, photographer_id: int,user_id:int):
    return db.query(models.Review).filter(models.Review.photographer_id == photographer_id,models.Review.user_id==user_id).all() 

def get_reviews_for_photo(db: Session, photo_id: int):
    return db.query(models.Review).filter(models.Review.photo_id == photo_id).all()

def get_reviews_for_photographer(db: Session, photographer_id: int):
    return db.query(models.Review).filter(models.Review.photographer_id == photographer_id).all() 