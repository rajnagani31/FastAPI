from fastapi import APIRouter , Request, Form
from typing import Annotated
from schema.user_schema import UserRegister,studentDetails,CourseDetails,markesDetails,LoginUser
from controller.user import user_register,create_student_details, user_login



router = APIRouter(tags=["User Authentication"])


@router.post("/user/register")
async def register_user(data : UserRegister , request: Request):
    "user registration endpoint"

    "all logic will be implemented via controllers"


    return await user_register(data,request)

@router.post("/user/login")
async def login_user(request: LoginUser):
    "user login endpoint"


    return await user_login(request)

@router.post('/user/student_details')
async def student_details(student_data: Annotated[studentDetails , Form()]):

    """student details endpoint does work with as user id,
    
    create student profile after create a first time account"""

    return await create_student_details(student_data)

@router.post('/user/course_details')
async def course_details():                 
    "course details endpoint"
    return {"message": "Course details endpoint"}

@router.post('/user/marks_details')
async def marks_details():               
    "marks details endpoint"
    return {"message": "Marks details endpoint"}




