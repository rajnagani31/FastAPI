from pydantic import BaseModel , EmailStr, field_validator,field_serializer,Field, model_serializer, model_validator
from enum import Enum   
from typing import Optional
import re
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

class ChangePassword(BaseModel):
    new_password : str
    confirm_new_password : str

    @model_validator(mode='after')
    def passwords_match(self):
        # password_pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#^~+=\(\)\-])[A-Za-z\d@$!%*?&#^~+=\(\)\-]{8,25}$")
        # if not password_pattern.match(self.new_password):
        #     raise ValueError("Password must be 8-25 characters long, include at least one uppercase letter, one lowercase letter, one digit, and one special character.")
        if self.new_password != self.confirm_new_password:
            raise ValueError("New password and confirm new password do not match")
        return self