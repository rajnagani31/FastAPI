from fastapi import APIRouter , HTTPException , status, Request
from fastapi.responses import JSONResponse
from sqlalchemy import select, update ,delete,and_,or_,distinct,func
from sqlalchemy.dialects.postgresql import insert  
from database import database
from database import user_details_table,student_details_table,course_details_table,new_validate_token_table
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

        stmt = insert(new_validate_token_table).values(
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
    
    
async def create_student_details(student_data,current_user): 
    "create student details controller"

    try:
        user_id = current_user
        student_name = student_data.student_name
        age = student_data.age
        address = student_data.address

        print("User ID in controller:", user_id)  # Debugging line to check the user_id value
        print("Student Name:", student_name)  # Debugging line to check the student_name value
        print("Age:", age)  # Debugging line to check the age value
        print("Address:", address)  # Debugging line to check the address value
        
        query = student_details_table.insert().values(
            user_id = int(user_id),
            student_name = student_name,
            age = age,
            address = address
        )
        student_data = await database.execute(query)

        data = {
            "user_id": user_id,
            "student_name": student_name,
            "age": age,
            "address": address
        }
        return JSONResponse(content=data,status_code=status.HTTP_201_CREATED)
    except Exception as e:
        return str(e)
    

async def get_student_data(current_user ):
    user_id = int(current_user)
    
    if not user_id:
        # return {"message": "user id not found", "status": 404}
        return JSONResponse(content="User id not found",status_code=status.HTTP_404_NOT_FOUND)

    query = (
        select(
            student_details_table,
            func.count().over().label('total_count')  # Window function to get total count
        ).where(
            student_details_table.c.user_id == user_id,
            student_details_table.c.student_name == "rajjjjj"
        )
        .limit(5)
        .offset(0)
    )

    distinctcount = (select(func.count(distinct(student_details_table.c.user_id)).label("count")).where(
        student_details_table.c.user_id == user_id
    ))

    distinctcountdata = await database.fetch_one(distinctcount)
    print("COUNT:", distinctcountdata['count']) # or distinctcountdata[0]

    result = await database.fetch_all(query)    
    
    if not result:
        return JSONResponse(content="Student details not found",status_code=status.HTTP_404_NOT_FOUND)
    print(result[0]['total_count'])
    if result:
        total_count = result[0]['total_count']
    else:
        total_count = 0
    # students = [
    #     {key: value for key, value in dict(row).items() if key != 'total_count'}
    #     for row in result
    # ] 

    students =[
        {
            "id": row['id'],
            "user_id": row['user_id'],  
            "student_name": row['student_name'],
            "age": row['age'],
            "address": row['address'],
            "created_at": str(row['create_at']),
            "updated_at": str(row['updated_at'])
        }
        for row in result
    ]
        
    # return JSONResponse(content=student_datas[:5], status_code=status.HTTP_200_OK)
    # return JSONResponse(content={"count": total_count, "data": students}, status_code=status.HTTP_200_OK)
    return {
        "total_count": total_count,
        "distinct_count": distinctcountdata['count'],
        "students": students
    }
async def student_course_details(course_details, current_user):
    try:

        user_id = int(current_user)
        course = course_details.course_name
        duration = course_details.course_duration
        fee = course_details.course_fee
        if not user_id:
            return JSONResponse(content="User id not found",status=400)

        query = course_details_table.insert().values(
            user_id = user_id,
            course_name = course,
            course_duration = duration,
            course_fee = fee
        )
        await database.execute(query)

        return JSONResponse(content="course detail filout",status_code=201)
    except Exception as e:
        return JSONResponse(status_code=500,content=f'ERROR {str(e)}')
    

async def change_user_password(data, current_user):
    try:
        user_id = int(current_user)
        new_password = data.new_password

        hase_new_password = hashlib.md5(new_password.encode()).hexdigest()

        query = update(user_details_table).where(
            user_details_table.c.id == user_id
        ).values(
            password = hase_new_password
        )

        await database.execute(query)

        return JSONResponse(content="Password changed successfully",status_code=200)
    
    except Exception as e:
        return JSONResponse(status_code=500,content=f'ERROR {str(e)}')
    
async def logout_user(current_user):
    try:
        user_id = int(current_user)
        if not user_id:
            return JSONResponse(content="User id not found",status=400)

        query = update(new_validate_token_table).where(
            new_validate_token_table.c.user_id == user_id,
            new_validate_token_table.c.token_type == "access"
        ).values(
            is_deleted = True
        )


        await database.execute(query)

        return JSONResponse(content="User logged out successfully",status_code=200)
    
    except (Exception,ValueError) as e:
        return JSONResponse(status_code=500,content=f'ERROR {str(e)}')