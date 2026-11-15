from pydantic import BaseModel, Field
from typing import List, Literal


class User(BaseModel):
    id: int
    name: str = Field(..., min_length=3, max_length=50)
    age: int = Field(..., gt=0, lt=150)
    sub : Literal["admin", "user", "guest"] = "user"

user = {"id" : 1, "name": "John Doe", "age": 30, "sub": "admin"}

user_data = User(**user)
print(user_data)

# TODO

class Product(BaseModel):
    id : int
    name : str 
    price : float
    in_stock : bool = False

product = {"id": 1, "name": "Laptop", "price": 999.99}
product_data = Product(**product)
print(product_data)