from sqlalchemy.orm import Session
from .. import models, schemas
from datetime import datetime, timezone

def create_share(db: Session, photo_id: int, from_user_id: int, to_user_id: int, expiry: datetime, link: str):
    share = models.Share(
        photo_id=photo_id,
        from_user_id=from_user_id,
        to_user_id=to_user_id,
        expiry=expiry,
        link=link
    )
    db.add(share)
    db.commit()
    db.refresh(share)
    return share

def get_share(db: Session, share_id: int):
    return db.query(models.Share).filter(models.Share.id == share_id).first()

def get_valid_share(db: Session, share_id: int):
    share = get_share(db, share_id)
    if share :
        expiry = share.expiry.replace(tzinfo=timezone.utc)
    if expiry > datetime.now(timezone.utc):
        return share
    return None 