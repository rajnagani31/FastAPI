from enum import Enum
from pydantic import BaseModel
from fastapi import APIRouter


router = APIRouter(tags=['rajja'])


class Name(str , Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"


class User(BaseModel):
    name : str
    status : Name



@router.post("/name/all_data")
def Name_status(status_data: Name = Name.active):
    if status_data is Name.inactive:
        return {
            "model":status_data,
            "status":200    
        }
    
    if status_data.value  == "suspended":
        return {
            "model":"suspended",
            "status":400,
        }
    return {"status": status_data}


@router.get("/get_details/{model_name}")
async def get_data(model_data : Name):  
    if model_data is Name.active:
        return {
            "status":200 ,
            "model":model_data
        }
    return model_data
    
@router.get("/{model_name}")
def data_get(mode_name : Name):
    

    return mode_name    