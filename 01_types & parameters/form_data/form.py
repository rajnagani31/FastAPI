from fastapi import APIRouter , Depends ,Form ,HTTPException ,Body
from schema.user_details_schema import user_login
from sqlalchemy.orm import Session
from database.database_confige import get_db
from model.user import Login
from typing import Annotated
routes = APIRouter(tags=["Form Data"])


@routes.post("/user/login")
def user_login_data(user_details : Annotated[user_login, Form()] , db : Session= Depends(get_db)):
    db_user = Login(user_name = user_details.user_name , password = user_details.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {
        "data":db_user
    }

@routes.get("/user/data")
def user_data(db:Session = Depends(get_db)):
    # result = db.query(Login).all()
    # result = db.query(Login  ).filter(Login.user_name == "string").all()
    result = db.get(Login , 3)
    return result


@routes.put("/user/update")
def user_data( user_id : int,user_details : Annotated[user_login , None],db:Session = Depends(get_db)):
    """
    also use this type
    
    user = db.query(Login).filter(Login.user_id == user_id).first()
    user.user_name = "kbc"
    """
    user = db.query(Login).filter(Login.user_id == user_id).update({"user_name":user_details.user_name , "password":user_details.password})
    db.commit()
    db.refresh(user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User updated successfully"}


@routes.post("/tast_user_for_form")
def user_data_test(name : str = Form() , age : int= Form() , body : int =  Body()):
    result = {"name":name , "age":age ,'body':body}
    return result

