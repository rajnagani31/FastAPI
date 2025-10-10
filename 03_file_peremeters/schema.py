from pydantic import BaseModel
from datetime import datetime
from fastapi import UploadFile


class   UserSchema(BaseModel):
    user_name : str 
    created_at : datetime | None = None
    updated_at : datetime | None = None

    
class UserFileDataBase(BaseModel):
    user_id: int
    # file_name: list[str] # list[UploadFile] This not valid stat becuse UploadFile is not a data type is FastAPI class For upload a file
    # file_type: str
    # file_size: int          # bytes
    # size_readable: str  

    