from pydantic import BaseModel , EmailStr, field_validator,field_serializer,Field
from enum import Enum   
from typing import Optional

class UserRegister(BaseModel):
    user_name : str
    email : EmailStr
    password: str
    confirm_password : str

    

class LoginUser(BaseModel):
    email :str
    password : str


class studentDetails(BaseModel):
    student_name : str
    age : int | None = None
    address : str | None = None 





class CourseNameEnum(str, Enum):
    AI = "AI"
    PYTHON = "Python"
    GENAI = "GenAI"

class CourseDetails(BaseModel):
    course_name : CourseNameEnum
    course_duration : str
    course_fee : float


class markesDetails(BaseModel):
    user_id : int
    course_id : int
    math_marks : float
    science_marks : float