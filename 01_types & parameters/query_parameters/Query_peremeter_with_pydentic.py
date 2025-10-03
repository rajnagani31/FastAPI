from pydantic import BaseModel , Field , constr
from fastapi import APIRouter , Query , Body , Path
from typing import Annotated ,Literal

routes = APIRouter(tags=["Query Parameters with pydentic validation"])

class FilterParams(BaseModel):
    limit : int = Field(le=10)
    offset : int = Field(0 , le=10)
    order_by : Literal['created_at' , 'updated_at'] = "created_at"
    tags : list[str] = []
    Mobile_phone : int

    model_config = {'extra':"forbid"}
    # v : int = constr(regex= 'j')

@routes.post("/FilterParams")
def Filter_data(filter_params: Annotated[FilterParams , Query()]):
    try:
        if len(str(filter_params.Mobile_phone)) != 10:
            print(filter_params)
            return {"error":"mobile number must be 10"}
        
    except Exception as e:
        return f"ERROR {e}"
    return filter_params 



class Item(BaseModel):
    name: str
    description: str | None = Field(default=None , description= " Items are good for kids")
    price: float | None =Field(default=None , title="Price must be float beacuse Tax included")
    tax: float | None = Field(title="Tax are all included")
    list_data : list[str] = None

class User(BaseModel):
    username: str
    full_name: str | None = None


@routes.put("/items/{item_id}")
async def update_item(
    item_id: int, item: Item, user: Annotated[User , Query()], importance: Annotated[int, Body()]
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results