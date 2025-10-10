# Crud schemas


from pydantic import BaseModel , EmailStr

class UserBase(BaseModel):
    email : EmailStr
    age : int | float
    name : str | None 


class CreateUser(UserBase):
    pass

class UserRead(UserBase):
    id : int

    class config:
        orm_mode = True

        