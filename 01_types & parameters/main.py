from fastapi import FastAPI ,Request
from typing import Annotated , get_args ,get_origin ,get_type_hints
from pydantic import BaseModel
from fastapi import APIRouter
from class_enum_with_path_parameters import router
from query_parameters.routes import routes as query_params
from query_parameters.Query_peremeter_with_pydentic import routes as pydentic_validation
from nested_parapeters.routes import routes as nested_model
from form_data.form import routes as user_details
from database.database_confige import engine
from model import user
from model.user import Base

class Name(BaseModel):
    user_id : int
    name : str

# data_base config
user.Base.metadata.create_all(bind = engine)


app = FastAPI()
app.include_router(router)
app.include_router(query_params)
app.include_router(pydentic_validation)
app.include_router(nested_model)
app.include_router(user_details)




# Tuple
def process_items(*items: tuple[str]):
    print(items)


process_items(1,2,3,'5',5.7)

# Optional | None

def home(name : str | None = None):
    if name is not None:
        print(f"Name is {name}")
    else:
        print("Name is None")

home()            


# classes as types

class person:
    def __init__(self , name):
        self.name = name

def get_person(name_person : person):
    return name_person        

print(get_person('raj'))


# annotated with parameter(query and path)

" with query params"
async def get_items(request : Request , user_id:Annotated[int,'enter a items ID']):
    return {
        "user_id":user_id,
        "method":request.method,
        "URL":str(request.url),
        "headers":dict(request.headers)
    }

" With get params"
@app.get("/get_name")
async def get_all_name(user_id : int , name : str):
    return {
        "id":user_id,
        "name":name
    }


@app.post("/name")
async def post_name(details:Name):
    print(details)
    return details




@app.get("/users")
async def read_users():
    return ["Rick", "Morty"]


@app.get("/users")
async def read_users2():
    
    return ["Bean", "Elfo"]    

