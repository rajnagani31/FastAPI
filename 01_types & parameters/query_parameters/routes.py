from fastapi import APIRouter , Body ,Query , HTTPException , Path
from typing import Annotated
from pydantic import BaseModel , validator

class items(BaseModel):
    n:str
    x:int
    y:int

class User(BaseModel):
    name : str
    age: int   


routes = APIRouter(tags=["query_parameters"])

@routes.post("/abcd" ,description="get all n and x data")
def get_data(n:int, x : int):
    return {"n":n , "x":x}

@routes.post("/kbc" ,description="get all n and x data")
def get_data(n:int, x : int):
    return {"n":n , "x":x}


@routes.post("/items/{item_id}" , description="data with optional and type(bool) parameters") 
def get_user_data(item_id ,item: items = Body(embed=True)  ,user_id :int | None = None , q:str | None = None , short : bool = False):
    if user_id is None:
        return {
            "status":400,
            "error":"Not Found User id"
        }
    return {
        "staus":200,
        "message":{
            "user_id":user_id,
            "data":q,
            "short":short,
            "item_id":item_id,
            "data":item
        }
    }

@routes.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    item_ : items ,user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id,**item_}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item



@routes.put("/body_data")
async def body_data(data : items = Body(embed=True)):
    # data = {"body_data":data}
    return data

@routes.put("/user_data")
async def user_data(user_id, item :items, user: User):
    return {'user_id':user_id ,"items":item , "user":user}  


@routes.get("/Query_with_validation/")
async def user(name :str| None = Query(max_length= 10)) -> dict:
    name = {"name": name}
    return name

@routes.post("/Query_with_Annoteted")
async def user(name: Annotated[str | None , Query(max_length = 10)] = None) -> dict:
    n ={"name":name}
    n.update({"x":300})
    return n

@routes.post("/Query_with_digit")
async def user(n: int | None = Query(max_digits=10)) -> dict:
    num = {"n":n}
    return num


@routes.get('/all_items/')
def read_items(q : Annotated[list[str] , Query(alias="pk")] = ['A','b',1]):
    data_items = {"q":q}
    return data_items   



class UserData(BaseModel):
    name : str
    age : int

    @validator("age")
    def age_must_be_positive(cls , v):
        if v <= 0:
            raise ValueError("Age must be positive")
        return v
    

@routes.get("/costom validation/")
def age_data(name: str , age : int):
    try:
        user = UserData(name = name , age = age)
        return user
    
    except ValueError as e:
        raise HTTPException(status_code=400,    detail=str(e))