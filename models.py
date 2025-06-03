from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, DateTime, Text, Enum, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from . import database

import enum

class UserType(str, enum.Enum):
    simple = "simple"
    photographer = "photographer"

class User(database.Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    user_type = Column(Enum(UserType), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    followers = relationship("Follow", back_populates="photographer", foreign_keys='Follow.photographer_id')
    following = relationship("Follow", back_populates="user", foreign_keys='Follow.user_id')
    photos = relationship("Photo", back_populates="owner")
    reviews = relationship("Review", back_populates="user",foreign_keys='Review.user_id')

    
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

class Follow(database.Base):
    __tablename__ = "follows"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    photographer_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="following", foreign_keys=[user_id])
    photographer = relationship("User", back_populates="followers", foreign_keys=[photographer_id])


class Photo(database.Base):
    __tablename__ = "photos"
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    file_path = Column(String, nullable=False)
    file_size= Column(Float, nullable=False)
    created_at = Column(DateTime)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="photos")


class Share(database.Base):
    __tablename__ = "shares"
    id = Column(Integer, primary_key=True, index=True)
    photo_id = Column(Integer, ForeignKey("photos.id", ondelete="cascade"))
    from_user_id = Column(Integer, ForeignKey("users.id"))
    to_user_id = Column(Integer, ForeignKey("users.id"))
    opened=Column(Boolean)
    expiry = Column(DateTime)
    link = Column(String)


class Review(database.Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id",ondelete="cascade"))
    photo_id = Column(Integer, ForeignKey("photos.id",ondelete="cascade"), nullable=True)
    photographer_id = Column(Integer, ForeignKey("users.id",ondelete="cascade"), nullable=True)
    user=relationship('User',back_populates="reviews",foreign_keys=[user_id])
    rating = Column(Float)
    comment = Column(Text)


class blacklist(database.Base):
    __tablename__='blacklists'
    id= Column(Integer,primary_key=True,index=True)
    blacklist_token= Column(String,unique=True,index=True)
    blacklist_on=Column(DateTime,server_default=func.now())


class MagicLink(database.Base):
    __tablename__ = "magic_links"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, index=True)
    token = Column(String, unique=True, nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    used = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
