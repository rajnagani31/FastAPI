from fastapi import APIRouter,Request,status,HTTPException,Query,Path,Header
from controller.user import register, login, logout, password_update
from schema.user import UserData, LoginUser,ChangePassword
from sqlalchemy.orm import Session  
from database_config import get_db  
from fastapi import Depends
from fastapi.responses import JSONResponse,Response
from dependencies import verify_token
from typing import Any,Annotated
from controller.admin import get_all_user
from services.admin_service import get_user


router = APIRouter(
    prefix="/v1/admin",
    tags=['admin']
)

@router.get('/get-user-list')
async def get_all_user_detail(request: Request, db:Annotated[Session, Depends(get_db)], current_user: str = Depends(verify_token)):
    " Get all user detail end-point with "
    try:
        print("user id",request.state.user_id)
        user_role = request.user_role
        if user_role in ('admin','superadmin','user'):
            print('run get API')

            return await get_all_user(db)
        return Response(status_code=status.HTTP_403_FORBIDDEN,content="Access forbidden: Admins only")  
        
    except Exception as e:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content="Internal server error")

@router.get('get-user_data/{id}')
def get_user_data_id(id, db:Annotated[Session,Depends(get_db)],token: Annotated[str,Query()] = None):
    if id:
       data =  get_user(user_id=id,db=db)

    if token:
        data = get_user(db=db,token=token)

    return Response(content=f"data get by id {data}",status_code=200)

    