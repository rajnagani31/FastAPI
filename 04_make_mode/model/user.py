from sqlalchemy import Column ,Integer , Table, Boolean, String, DateTime, Date, Text,ForeignKey, Time 
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


def user():
    user_table = Table(
        "user",
        Base.metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('first_name', String(50), nullable=False),
        Column('last_name', String(50), nullable=True),
        Column('ip_address', String(50), nullable=True),
        Column('email', String(50), nullable=True, unique=True),
        Column('user_profile', String(50), nullable=True),
        Column('mobile_number', Integer, nullable=True, unique=True),
        Column('designation', String(50), nullable=True),
        Column('is_active_', Boolean, default=True),
        Column('created_at', DateTime(timezone=True), server_default=func.now(), nullable=True),
        Column('date_of_birth', Date, nullable=True),
        Column('address', Text, nullable=True),
        Column("is_active", Boolean, default=True)
    )
    return user_table

def store():
    store_table = Table(
        "store",
        Base.metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('store_name', String(50), nullable=False),
        Column('store_location', String(50), nullable=True),
        Column('is_active_', Boolean, default=True),
        Column('created_at', DateTime(timezone=True), server_default=func.now(), nullable=True),
        Column("is_active", Boolean, default=True)
    )
    return store_table
    
def incidents():
    incidents = Table(
        "incidents",
        Base.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("store_id", Integer, ForeignKey("store.id") , nullable=True),
        Column("store_name", String(50), nullable=True),
        Column("data_of_incident", Date, nullable=True , server_default=func.current_date()),
        Column("time_of_incident", Time, nullable=True , server_default=func.current_time()),
        Column("location", String(50), nullable=True),
        Column("total_cameras_active",Integer, nullable=True),
        Column("Upload_video_file", String(50), nullable=True),
        Column("user_id",Integer, ForeignKey("user.id") , nullable=True),
        Column("create_at",DateTime(timezone=True), server_default=func.now(), nullable=True),
        Column("incident_type", String(50), nullable=True),
    )
    return incidents


def suspectsimages():
    suspectsimages = Table(
        "suspects_images",
        Base.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("incident_id", Integer, ForeignKey("incidents.id") , nullable=True),
        Column("suspects_images_file0", String(50), nullable=True),
        Column("link_type", String(50), nullable=True),
    )
    return suspectsimages

def liked_incidents():
    liked_incidents = Table(
        "liked_incidents",
        Base.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("incident_id", Integer, ForeignKey("incidents.id") , nullable=True),
        Column("like_type", String(50), nullable=True),
    )
    return liked_incidents

def witness_statements():
    witness_statements = Table(
        "withness_statements",
        Base.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("incident_id", Integer, ForeignKey("incidents.id") , nullable=True),
        Column("witness_statements",String(255), nullable=True),
        Column("Statement_date" , Date, nullable=True , server_default=func.current_date()),
        Column("witness_name", String(50), nullable=True),
        Column("witness_signature", String(50), nullable=True),
        Column("witness_age",String(50), nullable=True),    
        Column("witness_ocupation",String(50) ,nullable=True),
        Column("una",Integer, nullable=True),
    )
    return witness_statements
    
def video():
    video_data = Table(
        "video_data",
        Base.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("incident_id", Integer, ForeignKey("incidents.id") , nullable=True),
        Column("video_file", String(50), nullable=True),
        Column("video_description", String(255), nullable=True),
        Column("ref_number", String(50), nullable=True),
    )
    return video_data

def category():
    category = Table(
        "category",
        Base.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("Category", String(50), nullable=True),
    )
    return category

def policemaster():
    policemaster = Table(
        "policemaster",
        Base.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("Police_station_name", String(50), nullable=True),
        Column("Police_station_location", String(50), nullable=True),
        Column("Police_officer_name", String(50), nullable=True),
        Column("Police_officer_rank", String(50), nullable=True),
        Column("Contact_number", Integer, nullable=True),
        Column("Email_id", String(50), nullable=True),
    )
    return policemaster

def cases():
    cases = Table(
        "cases",
        Base.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("incident_id", Integer, ForeignKey("incidents.id") , nullable=True),
        Column("category_id", Integer, ForeignKey("category.id") , nullable=True),
        Column("police_id", Integer, ForeignKey("policemaster.id") , nullable=True),
        Column("case_number", String(50), nullable=True),
        Column("case_status", String(50), nullable=True),
        Column("assigned_officer", String(50), nullable=True),
        Column("remarks", String(255), nullable=True),
    )
    return cases

def casestatus():
    casestatus = Table(
        "casestatus",
        Base.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("case_id", Integer, ForeignKey("cases.id") , nullable=True),
        Column("status_update", String(255), nullable=True),
        Column("remark", Date, nullable=True , server_default=func.current_date()),
        Column("updated_by", String(50), nullable=True),
    )
    return casestatus

def suspects():
    suspects_table = Table(
        "suspects_info",
        Base.metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('suspect_image_id', Integer, ForeignKey("suspects_images.id") , nullable=True),
        Column('first_name', String(50), nullable=False),
        Column('last_name', String(50), nullable=True), 
        Column("gender", String(10), nullable=True),
        Column("athnicity", String(50), nullable=True),
        Column("bulic",String(50), nullable=True),
        Column("height",String(50), nullable=True),
        Column("toop",String(50), nullable=True),
        Column("bottom",String(50), nullable=True),
        Column("taatoo",String(50), nullable=True),
        Column("footwear",String(50), nullable=True),
        Column("pyshical_description",String(255),nullable=True),
        Column("remark",String(50),nullable=True),
    )

    return suspects_table


def example():
    example_table = Table(
        "example",
        Base.metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('name', String(50), nullable=False),
        Column('description', String(255), nullable=True),
    )
    return example_table