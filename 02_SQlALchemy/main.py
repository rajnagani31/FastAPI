from fastapi import FastAPI ,Depends ,HTTPException
from sqlalchemy.orm import Session
import model , schema, crud
from database import engin ,get_db ,base
from routs import routes as crud_api
#  create DB


model.base.metadata.create_all(bind =engin)

app = FastAPI(title="Fast API CRUD")
app.include_router(crud_api)
