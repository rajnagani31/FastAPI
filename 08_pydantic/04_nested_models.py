from tkinter import NO
from typing import List, AnyStr, Optional, Dict, Union, ForwardRef, TypeVar, Generic, NewType, Callable, Any
from pydantic import BaseModel


# nested models
class Address(BaseModel):
    street: str
    city: str
    country: str

class User(BaseModel):
    name: str
    age: int
    address: Address

# self referential models
class Comment(BaseModel):
    id : int
    content : str
    replies : List['Comment'] | None = None # or might be List['Comment'] = []

Comment.model_rebuild() # to resolve the forward reference for Comment in replies
Comment.update_forward_refs() # to resolve the forward reference for Comment in replies

a= '123'
print(list(a))