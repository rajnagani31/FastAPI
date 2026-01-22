from sqlalchemy import Column, Integer, String, Boolean,DateTime,DATE,func,ForeignKey,TEXT
from sqlalchemy.ext.declarative import declarative_base
from database_config import base


class ServerLogs(base):
    __tablename__ = "server_logs"

    id = Column(Integer,primary_key=True, index=True)
    user_id = Column(ForeignKey("user_auth.id"),nullable=True)
    user_role = Column(String(10),nullable=True)
    session_id = Column(String(255),nullable=True)
    user_ip = Column(String(255),nullable=True)
    api_method = Column(String(50),nullable=True)
    url = Column(String(1000),nullable=True)
    payload = Column(TEXT,nullable=True)
    token = Column(String(255),nullable=True)
    created_at = Column(String(100), server_default=func.now(), nullable=True)
    