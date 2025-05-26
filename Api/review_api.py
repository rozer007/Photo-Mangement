from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import dependencies,database,schemas
from ..Crud import review_crud,follow_crud,photo_crud

router = APIRouter()

@router.post("/reviews_photo")#, response_model=schemas.ReviewOut)
def add_review_photo(review: schemas.ReviewCreate_Photo, db: Session = Depends(database.get_db), current_user=Depends(dependencies.get_current_active_user)):
    if current_user.user_type !='simple':
        raise HTTPException(status_code=403, detail="Only simple user can review")
    
    following=follow_crud.get_following(db,current_user.id)
    photographer_ids = [f['photographer_id'] for f in following]
    Photos=[]
    for pid in photographer_ids:
        Photos.extend(photo_crud.get_photos_by_owner(db, pid))

    photos_id=[p.id for p in Photos]

    if not review.photo_id in photos_id:
        raise HTTPException(status_code=403, detail="No such photo exist/Not following this photographer")
    
    if review_crud.check_reviews_for_photo(db,review.photo_id,current_user.id):
        raise HTTPException(status_code=400, detail="Already Reviewed")

    return review_crud.create_review_photo(db,review,current_user)


@router.post("/reviews_photographer", response_model=schemas.ReviewOut)
def add_review_photographer(review: schemas.ReviewCreate_Photographer, db: Session = Depends(database.get_db), current_user=Depends(dependencies.get_current_active_user)):
    if current_user.user_type !='simple':
        raise HTTPException(status_code=403, detail="Only simple user can review")
    
    following=follow_crud.get_following(db,current_user.id)
    photographer_ids = [f['photographer_id'] for f in following]

    if not review.photographer_id in photographer_ids:
            raise HTTPException(status_code=403, detail="No such photo exist/Not following this photographer")
    
    if review_crud.check_reviews_for_photographer(db,review.photographer_id,current_user.id):
        raise HTTPException(status_code=400, detail="Already Reviewed")
    
    return review_crud.create_review_photographer(db,review,current_user)


@router.get("/photo/{photo_id}", response_model=list[schemas.ReviewOut])
def get_reviews_for_photo(photo_id: int, db: Session = Depends(database.get_db),current_user=Depends(dependencies.get_current_active_user)):
    owner=photo_crud.get_photo(db,photo_id)
    if current_user.id!= owner.owner_id:
        following=follow_crud.get_following(db,current_user.id)
        photographer_ids = [f['photographer_id'] for f in following]
        Photos=[]
        for pid in photographer_ids:
            Photos.extend(photo_crud.get_photos_by_owner(db, pid))

        photos_id=[p.id for p in Photos]

        if not photo_id in photos_id:
            raise HTTPException(status_code=403, detail="No such photo exist/Not following this photographer")

    return review_crud.get_reviews_for_photo(db, photo_id)

@router.get("/photographer/{photographer_id}", response_model=list[schemas.ReviewOut])
def get_reviews_for_photographer(photographer_id: int, db: Session = Depends(database.get_db),current_user=Depends(dependencies.get_current_active_user)):
    if current_user.id!= photographer_id:
        following=follow_crud.get_following(db,current_user.id)
        photographer_ids = [f['photographer_id'] for f in following]

        if not photographer_id in photographer_ids:
            raise HTTPException(status_code=403, detail="Not following this photographer")
        
    return review_crud.get_reviews_for_photographer(db, photographer_id)