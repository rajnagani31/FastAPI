from pydantic import BaseModel , EmailStr


class UserRegister(BaseModel):
    user_name : str
    email : EmailStr
    password: str
    confirm_password : str

    

class LoginUser(BaseModel):
    email :str
    password : str
