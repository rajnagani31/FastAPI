from fastapi import APIRouter,Request
from controller.user import register, login, logout, password_update
from schema.user import UserData, LoginUser,ChangePassword
from sqlalchemy.orm import Session  
from database_config import get_db  
from fastapi import Depends
from dependencies import verify_token
from typing import Any,Annotated
router = APIRouter(prefix="/user",tags=["Auth"])



@router.post('/register')
async def user_register(userdata: UserData,db:Session = Depends(get_db)):
    " User regsiter end-point with "

    return await register(userdata,db)


@router.post('/login')
async def user_login(userdata: LoginUser ,db:Session = Depends(get_db)):
    " User login end-point with "
    return await login(userdata,db)

@router.put('/change-password', dependencies=[Depends(verify_token)])
async def change_password(userdata: ChangePassword,request:Request, db:Annotated[Session, Depends(get_db)]): 
    current_user = request.state.user_id
    print("Current User ID:", current_user)
    " User update end-point with "
    return await password_update(userdata, current_user=current_user, db=db)

@router.post('/logout')
async def user_logout(request:Request, db:Annotated[Session, Depends(get_db)], current_user: str = Depends(verify_token)):
    " User logout end-point with "
    try:
        print("User ID from request state:", request.state.user_id)
        return await logout(current_user=current_user, db=db)
    except Exception as e:
        return {"message": "Error occurred during logout", "error": str(e)}
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzY5Mjc0MDg5LCJ0eXBlIjoiYWNjZXNzIn0.1H73w11H5Zn8l0ndVFib5hB4QKPGdIQQ-Mi3cgsyKsk