from fastapi import APIRouter
from fastapi import FastAPI ,Depends ,HTTPException
from sqlalchemy.orm import Session
import model , schema ,crud
from database import engin ,get_db 
from crud import Create_user, get_user,get_users,user_delete

routes = APIRouter()


@routes.post("/users/", response_model=schema.CreateUser)
async def create_user(user: schema.CreateUser, db: Session = Depends(get_db)):
    print('1')
    db_user = crud.Create_user(db, user)
    print('2')
    return db_user

@routes.get("/users/", response_model=list[schema.UserRead])
async def read_users(db: Session = Depends(get_db)):
    return get_users(db)

@routes.get("/users/{user_id}", response_model=schema.UserRead)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@routes.delete("/users/{user_id}")
async def delete_user_API(user_id: int, db: Session = Depends(get_db)):
    deleted = user_delete(db, user_id)
    if not deleted: 
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "deleted"}

@routes.put("/User_udate/{user_id}")
def user_update_data(user_id : int , user:schema.UserBase ,db : Session = Depends(get_db)):
    if user_id:
        if crud.update_user_details(db , user ,user_id):

            return "user Updetad"
        return "Id is not found"