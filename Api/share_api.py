from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta,timezone
from .. import database,dependencies,schemas
from ..Crud import share_crud

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
    print(datetime.now(timezone.utc))
    print(timedelta(minutes=expiry_minutes))
    print(datetime.now(timezone.utc)+timedelta(minutes=expiry_minutes))

    print(datetime.now(timezone.utc))


    link = f"share-{photo_id}-{to_user_id}-{int(expiry.timestamp())}"
    return share_crud.create_share(db, photo_id, current_user.id, to_user_id, expiry, link)

@router.get("/shared/{share_id}", response_model=schemas.ShareOut)
def get_shared_photo(share_id: int, db: Session = Depends(database.get_db), current_user=Depends(dependencies.get_current_active_user)):
    share = share_crud.get_valid_share(db, share_id)
    if not share:
        raise HTTPException(status_code=404, detail="Share not found or expired")
    # Only allow if current user is the recipient and follows the photographer
    if share.to_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to view this shared photo")
    return share 

@router.delete("/{share_id}",response_model=schemas.ShareOut)
def delete_shared_photo(share_id:int,db: Session = Depends(database.get_db), current_user=Depends(dependencies.get_current_active_user)):
    return share_crud.delete_share(db,share_id,current_user)