from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import dependencies,database,schemas
from ..Crud import review_crud,follow_crud,photo_crud,user_crud

router = APIRouter()

@router.post("/reviews_photo", response_model=schemas.ReviewOut_Photo)
def add_review_photo(review: schemas.ReviewCreate_Photo, db: Session = Depends(database.get_db), current_user=Depends(dependencies.get_current_active_user)):
    if current_user.user_type !='simple':
        raise HTTPException(status_code=403, detail="Only simple user can review")
    
    photos_id=photo_crud.users_following_photos_id(db,current_user)

    if not review.photo_id in photos_id:
        raise HTTPException(status_code=403, detail="No such photo exist/Not following this photographer")
    
    if review_crud.check_reviews_for_photo(db,review.photo_id,current_user.id):
        raise HTTPException(status_code=400, detail="Already Reviewed")

    return review_crud.create_review_photo(db,review,current_user)


@router.post("/reviews_photographer", response_model=schemas.ReviewOut_Photographer)
def add_review_photographer(review: schemas.ReviewCreate_Photographer, db: Session = Depends(database.get_db), current_user=Depends(dependencies.get_current_active_user)):
    if current_user.user_type !='simple':
        raise HTTPException(status_code=403, detail="Only simple user can review")
    
    following=follow_crud.get_following(db,current_user.id)
    photographer_ids = [f['photographer_id'] for f in following]

    if not review.photographer_id in photographer_ids:
            raise HTTPException(status_code=403, detail="Not following this photographer")
    
    if review_crud.check_reviews_for_photographer(db,review.photographer_id,current_user.id):
        raise HTTPException(status_code=400, detail="Already Reviewed")
    
    return review_crud.create_review_photographer(db,review,current_user)


@router.get("/photo/{photo_id}", response_model=list[schemas.ReviewOut_Photo])
def get_reviews_for_photo(photo_id: int, db: Session = Depends(database.get_db),current_user=Depends(dependencies.get_current_active_user)):
    photo=photo_crud.get_photo(db,photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="No such photo")
    
    if current_user.id!= photo.owner_id:
        if(current_user.user_type=='photographer'):
            raise HTTPException(status_code=403, detail="Not allowed to view review of this photo")

        photos_id=photo_crud.users_following_photos_id(db,current_user)

        if not photo_id in photos_id:
            raise HTTPException(status_code=403, detail="No such photo exist/Not following this photographer")

    reviews= review_crud.get_reviews_for_photo(db, photo_id)
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews for this photo")
    
    return reviews


@router.get("/photographer/{photographer_id}", response_model=list[schemas.ReviewOut_Photographer])
def get_reviews_for_photographer(photographer_id: int, db: Session = Depends(database.get_db),current_user=Depends(dependencies.get_current_active_user)):
    user=user_crud.get_user_by_userid(db,photographer_id)

    if not user or user.user_type!='photographer':
        raise HTTPException(status_code=404, detail="No such photographer")
    
    if current_user.id!= photographer_id:
        if(current_user.user_type=='photographer'):
            raise HTTPException(status_code=403, detail="Cannot view other photographer's review")
        
        following=follow_crud.get_following(db,current_user.id)
        photographer_ids = [f['photographer_id'] for f in following]

        if not photographer_id in photographer_ids:
            raise HTTPException(status_code=403, detail="Not following this photographer")
        
    return review_crud.get_reviews_for_photographer(db, photographer_id) 

@router.delete("/photographer/{photographer_id}", response_model=schemas.ReviewOut_Photographer)
def delete_reviews_for_photographer(photographer_id: int, db: Session = Depends(database.get_db),current_user=Depends(dependencies.get_current_active_user)):
   return review_crud.delete_photographer_review(db,photographer_id,current_user.id)

@router.delete("/photos/{photo_id}", response_model=schemas.ReviewOut_Photo)
def delete_reviews_for_photo(photo_id: int, db: Session = Depends(database.get_db),current_user=Depends(dependencies.get_current_active_user)):
   return review_crud.delete_photo_review(db,photo_id,current_user.id)