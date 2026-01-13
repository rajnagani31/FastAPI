from fastapi import APIRouter , Request, Form, Depends
from typing import Annotated
from schema.user_schema import UserRegister,studentDetails,CourseDetails,markesDetails,LoginUser
from controller.user import user_register,create_student_details, user_login, get_student_data, student_course_details
from utils import verify_token



router = APIRouter(tags=["User Authentication"])


@router.post("/user/register")
async def register_user(data : UserRegister , request: Request):
    "user registration endpoint"

    "all logic will be implemented via controllers"


    return await user_register(data,request)

@router.post("/user/login")
async def login_user(request: LoginUser):
    """ user login endpoint 
    
    return JWT access token and refresh token
    store the access token in the database table"""


    return await user_login(request)

@router.post('/user/student_details')
async def student_details(student_data: Annotated[studentDetails , Form()], current_user: str = Depends(verify_token)):

    """student details endpoint does work with as user id,
    
    create student profile after create a first time account"""

    return await create_student_details(student_data,current_user)

@router.get('/get-sudent-details')
async def get_student_details(current_user: str = Depends(verify_token)):
    """ Get loged in user detais data """

    return await get_student_data(current_user)

@router.post('/user/course_details')
async def course_details(course_details : Annotated[CourseDetails, Form()], current_user : str = Depends(verify_token)):                 
    "course details endpoint for student chosse favorite course details"
    return await student_course_details(course_details, current_user)

@router.post('/user/marks_details')
async def marks_details():               
    "marks details endpoint"
    return {"message": "Marks details endpoint"}




