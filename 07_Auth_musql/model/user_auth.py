from sqlalchemy import Column, Integer, String, Boolean,DateTime,DATE,func,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from database_config import base

class UserAuth(base):
    __tablename__ = "user_auth"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    session_id = Column(String(50),nullable=True)
    user_role = Column(String(50), default="user")
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(String(100), server_default=func.now(), nullable=True)
    updated_at = Column(String(100), onupdate=func.now(), nullable=True)
    last_login = Column(DateTime, nullable=True)

class UserToken(base):
    __tablename__ = "user_toke"

    id = Column(Integer,primary_key=True,index= True)
    user_id = Column(ForeignKey("user_auth.id"),nullable=True)
    token = Column(String(255),nullable=True)
    token_type = Column(String(10),default="access",nullable=True)
    is_deleted = Column(Boolean,default=False,nullable=True)





