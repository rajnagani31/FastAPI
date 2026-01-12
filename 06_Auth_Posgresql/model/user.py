from sqlalchemy import Column ,Table,Integer,String ,Boolean, Float, BigInteger ,ForeignKey ,DATE,Time,TIME,DateTime,UniqueConstraint
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
    user_token=Table(
    "user_token",
    metadata,
    Column('id',Integer,primary_key=True, autoincrement=True),
    Column('user_id',Integer,ForeignKey("user_details.id")),
    Column("token",String(255),nullable=False),
    Column("is_deleted",Boolean,nullable=True),
    Column('token_type',String(50),nullable=True),
    Column('create_at',DateTime(timezone=True),server_default=func.now()),
    Column('updated_at',DateTime(timezone=True),server_default=func.now()),
    UniqueConstraint('user_id', 'token_type', name='uq_user_token_user_id_token_type')
    )

    return user_token

def student_details(metadata):
    student_table=Table(
    "student_details",
    metadata,
    Column('id',Integer , primary_key = True , autoincrement=True),
    Column('user_id',Integer,ForeignKey("user_details.id")),
    Column('student_name',String(50), nullable=True),
    Column('age',Integer,nullable=True),
    Column('address',String(100),nullable=True),
    Column('create_at',DateTime(timezone=True),server_default=func.now(),nullable=True),
    Column('updated_at',DateTime(timezone=True),server_default=func.now(),nullable=True),
    )

    return student_table

def course_details(metadata):
    course_table=Table(
    "course_details",
    metadata,
    Column('id',Integer , primary_key = True , autoincrement=True),
    Column('user_id',Integer,ForeignKey("user_details.id")),
    Column('course_name',String(50), nullable=True),
    Column('course_duration',String(50),nullable=True),
    Column('course_fee',Float,nullable=True),
    Column('create_at',DateTime(timezone=True),server_default=func.now(),nullable=True),
    Column('updated_at',DateTime(timezone=True),server_default=func.now(),nullable=True),
    )

    return course_table

def markes_details(metadata):
    markes_table=Table(
    "markes_details",
    metadata,
    Column('id',Integer , primary_key = True , autoincrement=True),
    Column('student_id',Integer,ForeignKey("student_details.id")),
    Column('course_id',Integer,ForeignKey("course_details.id")),
    Column('math',Float,nullable=True),
    Column('science',Float,nullable=True),
    Column('history',Float,nullable=True),
    Column('total_marks',Float,nullable=True),
    Column('percentage',Float,nullable=True),
    Column('create_at',DateTime(timezone=True),server_default=func.now(),nullable=True),
    Column('updated_at',DateTime(timezone=True),server_default=func.now(),nullable=True),
    )

    return markes_table