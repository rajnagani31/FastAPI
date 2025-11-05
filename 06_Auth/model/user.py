from sqlalchemy import Column ,Table,Integer,String ,Boolean, Float, BigInteger ,ForeignKey ,DATE,Time,TIME,DateTime
from sqlalchemy.sql import func


def user_register(metadata):
    user_table =Table(
    "user_details",
    metadata,
    Column('id',Integer , primary_key = True , autoincrement=True),
    Column('user_name',String(50), nullable=True),
    Column('Email',String(50),nullable=True),
    Column('password',String(50),nullable=True),
    Column('first_name',String(50),nullable=True),
    Column('last_name',String(50),nullable=True),
    Column('is_active',Boolean,nullable=True , default=True),
    Column('is_delete',Boolean,nullable=True , default=False),
    Column('create_at',DateTime(timezone=True),server_default=func.now(),nullable=True),
    Column('updated_at',DateTime(timezone=True),server_default=func.now(),nullable=True),
    Column('role',String(50),default='user',nullable=True),
    
    Column("ip_address", String(20), nullable=True),
    )
    return user_table

def validate_token(metadata):
    user_token=(
    "user_token",
    metadata,
    Column('id',primary_key=True,autoincrement=True),
    Column('user_id',Integer,ForeignKey("user_details.id")),
    Column("toke",String(255),default=True),
    Column("is_deleted",Boolean,nullable=True),
    )

    return user_token