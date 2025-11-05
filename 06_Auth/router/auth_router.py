from fastapi import APIRouter , Request
from schema.user_schema import UserRegister
from controller.user import user_register



router = APIRouter(tags=["User Authentication"])


@router.post("/user/register")
async def register_user(data : UserRegister , request: Request):
    "user registration endpoint"

    "all logic will be implemented via controllers"


    return await user_register(data,request)