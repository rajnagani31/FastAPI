from pydantic import BaseModel


class image(BaseModel):
    url : str
    name : str


class details(BaseModel):
    price : float 
    age : int | None = None
    Tax : int | None = None
    description: str
    user : image | None = None
