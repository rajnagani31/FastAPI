from fastapi import FastAPI, Depends ,Body ,HTTPException
from typing import Annotated , Any
from depens import get_query_param
from database.config import get_db
from database import model
from schema.user import UserBase
from sqlalchemy.orm import Session
from database.config import engine
from sqlalchemy import exists,select
from routers.decoretor_depends import router as decoretor_router

app = FastAPI()
app.include_router(decoretor_router)

model.Base.metadata.create_all(bind=engine)

comman_need = Annotated[dict , Depends(get_query_param)]

@app.get("/details_with_depends")
async def read_details(data : comman_need):
    return data

# @get_query_param  
async def simple_endpoint(data : Annotated[UserBase, Depends(UserBase),Body()]):
    return {"data": data}


@app.post("/create_user")
async def create_user(user_ : UserBase , db :Annotated[Session , Depends(get_db)]):

    # user cheak
    user = db.query(model.User).filter(model.User.email == user_.email).first()

    # --> scaler
    user_with_scaler = db.scalar(select(exists().where(model.User.email == user_.email)))
    if user:
        raise HTTPException(status_code=400 , detail="User already exists")
    
    """ With scaler for cheak exists"""
    # if user_with_scaler:
    #     return {"statue":400,"message" : "User already exists"}
    
    db_user = model.User(name = user_.name , email = user_.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    data = {"message" : "User created successfully"}
    return data


