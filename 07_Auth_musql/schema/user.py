from pydantic import BaseModel , EmailStr, field_validator,field_serializer,Field, model_serializer, model_validator
from enum import Enum   
from typing import Optional
import re


class UserData:
    username : str 
    email : EmailStr
    password : str

    