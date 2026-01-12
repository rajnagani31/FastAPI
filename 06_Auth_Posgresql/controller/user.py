from fastapi import APIRouter , HTTPException , status, Request
from fastapi.responses import JSONResponse
from sqlalchemy import select, update ,delete,and_,or_
from sqlalchemy.dialects.postgresql import insert  

from database import database
from database import user_details_table,user_jwt_token_table,student_details_table,markes_details_table,course_details_table
import hashlib
from utils import access_token,refresh_token


async def user_register(data , request):
    "user registration controller"
    try:
        username = data.user_name
        email = data.email  
        password = data.password
        confirm_password = data.confirm_password
        # ip_address = request.client.host
        x_forwarded_for = request.headers.get('x-forwarded-for')
        ip_address = x_forwarded_for.split(',')[0] if x_forwarded_for else request.client.host

        db_user = await database.fetch_one(select(user_details_table).where(user_details_table.c.Email == email))
        # user check
        if db_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="User already exists")
        
        if password != confirm_password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="Password and Confirm Password do not match")
        
        hase_password = hashlib.md5(password.encode()).hexdigest()

        query = user_details_table.insert().values(
            user_name = username,
            Email = email,
            password = hase_password,
            ip_address = ip_address,
        )

        await database.execute(query)
        return {"message": "User registered successfully"}
    
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail=str(e))
    

async def user_login(request):
    try:
        email = request.email
        password = request.password
        pass_hase = hashlib.md5(password.encode()).hexdigest()

        user = select(user_details_table).where(
            user_details_table.c.Email == email,
            user_details_table.c.password == pass_hase
        )

        user_row = await database.fetch_one(user)

        if not user_row:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        

        user_id = user_row['id']
        create_access_token = access_token(user_id)
        create_refresh_token = refresh_token(user_id)

        stmt = insert(user_jwt_token_table).values(
            user_id = user_id,  
            token = create_access_token,
            is_deleted = False,
            token_type = "access",
        )
        # UPSERT query
        upsert_query = stmt.on_conflict_do_update(
            index_elements=["user_id", "token_type"],
            set_={
                "token": create_access_token,
                "is_deleted": False
            }
        )

        await database.execute(upsert_query)

        data = {
            "message":"Login successfully",
            "Token":{
                "access_token":create_access_token,
                "refresh_token":create_refresh_token
            }
        }

        return JSONResponse(status_code=200, content=data)
    
    except HTTPException:
        raise

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": "Internal Server Error", "error": str(e)}
        )
    
    
async def create_student_details(student_data): 
    "create student details controller"

    try:
        user_id = student_data.user_id
        student_name = student_data.student_name
        age = student_data.age
        address = student_data.address

        query = student_details_table.insert().values(
            user_id = user_id,
            student_name = student_name,
            age = age,
            address = address,
        )

        await database.execute(query)
        return {"message": "Student details created successfully"}
    except Exception as e:
        return e