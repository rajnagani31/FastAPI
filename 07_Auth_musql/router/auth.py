from fastapi import APIRouter
from controller.user import *
from schema.user import UserData

router = APIRouter(prefix="/user",tags=["Auth"])



@router.post('/register')
async def user_register(userdata: UserData):
    " User regsiter end-point with "

    return await register(userdata)