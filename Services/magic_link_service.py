from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import HTTPException, status
from datetime import datetime, timedelta,timezone
import secrets
import pytz
from .. import database,models
from ..config import MAGIC_LINK_EXPIRE_MINUTES

def create_magic_link_token():
    return secrets.token_urlsafe(32)

def generate_magic_link(email:str,db:Session):
    db.query(models.MagicLink).filter(
        models.MagicLink.email==email,
        models.MagicLink.used=='False'
    ).update({'used':True})

    magic_token= create_magic_link_token()
    expires_at=datetime.now(timezone.utc) + timedelta(days=MAGIC_LINK_EXPIRE_MINUTES)

    magic_link=models.MagicLink(
        email=email,
        token=magic_token,
        expires_at=expires_at
    )

    db.add(magic_link)
    db.commit()
    db.refresh(magic_link)

    #create magic link url
    magic_link_url=f'http://127.0.0.1:8000/auth/verify_login?token={magic_token}'
    # http://127.0.0.1:8000/docs#/Authentication/magic_login_link_auth_magic_link_post

    return magic_token,magic_link_url

def verify_magic_token(token:str,db:Session):
    magic_link=db.query(models.MagicLink).filter(
        models.MagicLink.token==token,
        models.MagicLink.used==False
    ).first()

    if not magic_link:
        raise HTTPException(status_code=401, detail="No such magic link")
    
    india_tz = pytz.timezone('Asia/Kolkata')
    # Convert UTC expiry to India time
    expiry = magic_link.expires_at.astimezone(india_tz)
    india_time = datetime.now(india_tz)

    if expiry<india_time:
        raise HTTPException(status_code=403, detail="Link expires")
    magic_link.used=True
    db.commit()

    return magic_link.email


# def authenticate_through_magiclink():
