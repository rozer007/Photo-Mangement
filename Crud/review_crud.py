from sqlalchemy.orm import Session
from fastapi import HTTPException
from .. import models, schemas

def create_review_photo(db: Session, review: schemas.ReviewOut_Photo,current_user):
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

def create_review_photographer(db: Session, review: schemas.ReviewOut_Photographer,current_user):
    
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
    return db.query(models.Review).filter(models.Review.photo_id == photo_id,models.Review.user_id==user_id).first() 

def check_reviews_for_photographer(db: Session, photographer_id: int,user_id:int):
    return db.query(models.Review).filter(models.Review.photographer_id == photographer_id,models.Review.user_id==user_id).first() 

def get_reviews_for_photo(db: Session, photo_id: int):
    return db.query(models.Review).filter(models.Review.photo_id == photo_id).all()

def get_reviews_for_photographer(db: Session, photographer_id: int):
    return db.query(models.Review).filter(models.Review.photographer_id == photographer_id).all() 

def delete_photographer_review(db: Session, photographer_id: int,user_id:int):
    review=check_reviews_for_photographer(db,photographer_id,user_id)
    if not review:
        raise HTTPException(status_code=403, detail="No reviews")
    
    db.delete(review)
    db.commit()
    return review

def delete_photo_review(db: Session, photo_id: int,user_id:int):
    review=check_reviews_for_photo(db,photo_id,user_id)
    if not review:
        raise HTTPException(status_code=403, detail="No reviews ")
    
    db.delete(review)
    db.commit()
    return review