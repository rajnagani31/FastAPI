from fastapi import APIRouter , Request, Form, Depends
from typing import Annotated
from schema.user_schema import UserRegister,studentDetails,CourseDetails,markesDetails,LoginUser,ChangePassword
from controller.user import user_register,create_student_details, user_login, get_student_data, student_course_details, change_user_password,logout_user
from utils import verify_token, fack_dependency



router = APIRouter(tags=["User Authentication"])


@router.post("/user/register")
async def register_user(data : UserRegister , request: Request):
    "user registration endpoint"

    "all logic will be implemented via controllers"


    return await user_register(data,request)

@router.post("/user/login", description="will be use this credential when you use this api email raj@1234.com, password 1234")
async def login_user(request: LoginUser):
    """ user login endpoint 
    
    return JWT access token and refresh token
    store the access token in the database table"""


    return await user_login(request)

@router.post('/user/student_details')
async def student_details(student_data: Annotated[studentDetails , Form()], current_user: str = Depends(verify_token, use_cache=False), fack_user: str = Depends(fack_dependency)):

    """student details endpoint does work with as user id,
    
    create student profile after create a first time account"""

    return await create_student_details(student_data,current_user)

@router.get('/get-sudent-details')
async def get_student_details(current_user: str = Depends(verify_token), request: Request = None):
    """ get student details endpoint"""

    session_id = request.cookies.get("session_id")
    print("Session ID from cookie:", session_id)
    """ Get loged in user detais data """

    return await get_student_data(current_user)

@router.post('/user/course_details')
async def course_details(course_details : Annotated[CourseDetails, Form()], current_user : str = Depends(verify_token)):                 
    "course details endpoint for student chosse favorite course details"
    return await student_course_details(course_details, current_user)

@router.post('/change-password')
async def change_password(data : ChangePassword, current_user : str = Depends(verify_token)):
    "change password endpoint"
    return await change_user_password(data, current_user)


@router.post('/user-logout')
async def user_logout(current_user: str = Depends(verify_token)):
    """ User logout endpoint 
    will be soft delete the token from the database table
    """
    return await logout_user(current_user)
# @router.mount('/docs', custom_swagger_ui_html)
# def custom_swagger_ui_html(data: Request):
#     from fastapi.openapi.docs import get_swagger_ui_html
#     return get_swagger_ui_html(openapi_url="/openapi.json", title="Custom API Docs")




