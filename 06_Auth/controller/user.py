from fastapi import APIRouter , HTTPException , status, Request
from sqlalchemy import select , insert , update ,delete 
from database import database
from database import user_details_table,user_jwt_token_table
import hashlib



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

        db_user = await database.fetch_one(select(user_details_table).where(user_details_table.c.Email   == email))
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
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail=str(e))