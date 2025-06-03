from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from PIL import Image
from datetime import datetime, timedelta,timezone
from .. import database,dependencies,schemas
from ..Crud import share_crud,photo_crud

router = APIRouter()

@router.post("/share", response_model=schemas.ShareOut)
def share_photo(
    photo_id: int,
    to_user_id: int,
    expiry_minutes: int,
    db: Session = Depends(database.get_db),
    current_user=Depends(dependencies.get_current_active_user)
):
    
    expiry = datetime.now(timezone.utc) + timedelta(minutes=expiry_minutes)
    opened=False
    link = f"share-{photo_id}-{to_user_id}-{int(expiry.timestamp())}"
    return share_crud.create_share(db, photo_id, current_user.id,to_user_id,opened,expiry, link)

@router.get("/shared/{share_id}", response_model=schemas.ShareOut)
def get_shared_photo(share_id: int, db: Session = Depends(database.get_db), current_user=Depends(dependencies.get_current_active_user)):
    share = share_crud.get_valid_share(db, share_id)
    if not share:
        raise HTTPException(status_code=404, detail="Share not found or expired")
    # Only allow if current user is the recipient and follows the photographer
    if share.to_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to view this shared photo")
    
    photo=photo_crud.get_photo(db,share.photo_id)
    if photo.owner_id!=current_user.id:
        if current_user.user_type=="photographer":
            raise HTTPException(status_code=403, detail="This photo belongs to other photographer")
        photos_ids=photo_crud.users_following_photos_id(db,current_user)
        if share.photo_id not in photos_ids:
            raise HTTPException(status_code=403, detail="Not following the photographer")
    

    img=Image.open(photo.file_path)
    img.show()

    share.opened=True
    db.commit()

    return share 

@router.delete("/{share_id}",response_model=schemas.ShareOut)
def delete_shared_photo(share_id:int,db: Session = Depends(database.get_db), current_user=Depends(dependencies.get_current_active_user)):
    return share_crud.delete_share(db,share_id,current_user)