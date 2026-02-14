from pydantic import BaseModel , EmailStr, field_validator,field_serializer,Field, model_serializer, model_validator
from enum import Enum   
from typing import Optional
import re


class UserData(BaseModel):
    username : str 
    email : EmailStr
    password : str

class LoginUser(BaseModel):
    email: EmailStr
    password: str


class ChangePassword(BaseModel):
    new_password: str
    confirm_password: str

    @model_validator(mode='after')
    def passwords_match(self):
        if self.new_password != self.confirm_password:
            raise ValueError("New password and confirm password do not match")
        return self
    