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
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    followers = relationship("Follow", back_populates="photographer", foreign_keys='Follow.photographer_id')
    following = relationship("Follow", back_populates="user", foreign_keys='Follow.user_id')
    # photos = relationship("Photo", back_populates="owner")
    # reviews = relationship("Review", back_populates="user")

    
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

class Follow(database.Base):
    __tablename__ = "follows"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    photographer_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="following", foreign_keys=[user_id])
    photographer = relationship("User", back_populates="followers", foreign_keys=[photographer_id])

