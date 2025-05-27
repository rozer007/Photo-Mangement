from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..Crud import user_crud,photo_crud
from ..Services import ai_service
from .. import schemas,database,models
from .. import dependencies


router =APIRouter()

@router.get('/Generate_description/{photo_id}')
def generate_image_description(photo_id:int,db: Session = Depends(database.get_db),current_user=Depends(dependencies.get_current_active_user)):
    photo=photo_crud.get_photo(db,photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="No such photo")
    
    if current_user.id!=photo.owner_id:
        photo_ids=photo_crud.users_following_photos_id(db,current_user)

        if not photo_id in photo_ids:
            raise HTTPException(status_code=403, detail="No such photo exist/Not following this photographer")
    
    return ai_service.generate_description(photo.file_path)

@router.get('/generate_tag/{photo_id}')
def generate_image_description(photo_id:int,db: Session = Depends(database.get_db),current_user=Depends(dependencies.get_current_active_user)):
    photo=photo_crud.get_photo(db,photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="No such photo")
    
    if current_user.id!=photo.owner_id:
        photo_ids=photo_crud.users_following_photos_id(db,current_user)

        if not photo_id in photo_ids:
            raise HTTPException(status_code=403, detail="No such photo exist/Not following this photographer")
    
    return ai_service.generate_tags(photo.file_path)
