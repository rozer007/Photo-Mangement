from sqlalchemy.orm import Session
from fastapi import HTTPException
import os
from .. import models, schemas
from datetime import datetime,timezone

def create_photo(db: Session, photo: schemas.PhotoCreate, owner_id: int, file_path: str):
    db_photo = models.Photo(
        file_path=file_path,
        description=photo.description,
        tags=photo.tags,
        file_size=photo.file_size,
        created_at=datetime.now(timezone.utc),
        owner_id=owner_id
    )
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo


def delete_photo(db: Session, photo_id: int, owner_id: int):
    photo = db.query(models.Photo).filter(models.Photo.id == photo_id, models.Photo.owner_id == owner_id).first()
    if photo:
        if os.path.exists(photo.file_path):
            os.remove(photo.file_path)
            file_deleted = True
        else:
            file_deleted = False

        if not file_deleted:
            raise HTTPException(status_code=404, detail="Error while fetching the Photo from database")
        
        if file_deleted:
            db.delete(photo)
            db.commit()
            return photo
        else:
            return None
    else:
        return None
    
    
def get_photo(db: Session, photo_id: int):
    return db.query(models.Photo).filter(models.Photo.id == photo_id).first()

def get_photos_by_owner(db: Session, owner_id: int):
    return db.query(models.Photo).filter(models.Photo.owner_id == owner_id).all()