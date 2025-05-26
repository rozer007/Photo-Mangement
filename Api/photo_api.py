from fastapi import Depends, HTTPException, APIRouter,File ,UploadFile
from sqlalchemy.orm import Session
from ..Crud import photo_crud,follow_crud
from .. import dependencies
from .. import schemas,database
from .. Services import storage, ai
router=APIRouter()

@router.post("/upload")
def upload_photo(
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    current_user=Depends(dependencies.get_current_photographer)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File is not an image")
    
    photo_file = storage.save_photo(file)
    size =photo_file[1]
    file_path= photo_file[0]
    # AI add-ons
    tags = ai.generate_tags(file_path)
    description = ai.generate_description(photo_file[0])
    photo = schemas.PhotoCreate(
        tags = tags,
        description = description,
        file_size=size

    )
    return photo_crud.create_photo(db, photo, current_user.id, file_path)


@router.delete("/{photo_id}", response_model=schemas.PhotoOut)
def delete_photo(photo_id: int, db: Session = Depends(database.get_db), current_user=Depends(dependencies.get_current_photographer)):
    photo = photo_crud.delete_photo(db, photo_id, current_user.id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found or not owned by you")
    return photo 


@router.get("/feed", response_model=list[schemas.PhotoOut])
def get_feed(db: Session = Depends(database.get_db), current_user=Depends(dependencies.get_current_active_user)):
    if not current_user.user_type == 'simple':
        raise HTTPException(status_code=403, detail="Must be simple user")
    following = follow_crud.get_following(db, current_user.id)
    photographer_ids = [f['photographer_id'] for f in following]
    photos = []
    for pid in photographer_ids:
        photos.extend(photo_crud.get_photos_by_owner(db, pid))
    return photos

    
'''
@router.get("/{photo_id}", response_model=schemas.PhotoOut)
def get_photo(photo_id: int, db: Session = Depends(dependencies.get_db), current_user=Depends(dependencies.get_current_active_user)):
    photo = photo_crud.get_photo(db, photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    # Only allow if user follows the photographer
    if photo.owner_id != current_user.id:
        following = follow_crud.get_following(db, current_user.id)
        if not any(f.photographer_id == photo.owner_id for f in following):
            raise HTTPException(status_code=403, detail="Not allowed to view this photo")
    return photo


'''