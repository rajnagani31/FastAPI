from sqlalchemy.orm import Session
from services.user_service import create_user,get_user_by_email,insert_token,update_password,logout_user
from fastapi import HTTPException,status, Depends
from fastapi.responses import JSONResponse
from dependencies import verify_token,access_token,refresh_token
import hashlib


def data():
    print("Data function called")
    print("User registration process ongoing...")
    print("Preparing to create user...")


async def register(user_data,db:Session):
     
    try:

        username = user_data.username
        email = user_data.email
        password = user_data.password

        user = create_user(username, email, password, db)


        if not user:
            return {"message": "User not registered", "user": user_data}    
        
        return {"message": "User registered", "user": user_data}    
    
    except Exception as e:
        return {"message": "Error occurred during registration", "error": str(e)}
    

async def login(userdata, db:Session):
    try:
        email = userdata.email
        password = userdata.password

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        user = get_user_by_email(email, hashed_password, db)  # You need to pass the actual DB session here

        if not user:
            return JSONResponse(status_code=400,content={"message": "Invalid email or password"})
        
        access_token_str = access_token(user.id)
        refresh_token_str = refresh_token(user.id)
        
        message = {
            "message": "Login successful",
            "Tokens": {
                "access_token": access_token_str,
                "refresh_token": refresh_token_str  
            }
        }
        insert_token(user.id, access_token_str, db)
        
        return JSONResponse(status_code=200,content=message)

    except Exception as e:
        return {"message": "Error occurred during login", "error": str(e)}  


async def logout(current_user: str, db:Session):
    try:
        user = logout_user(int(current_user), db)
        print("Logout function - User:", user)
        if user is None:
            return JSONResponse(status_code=404,content={"message": "User not found"})
        return JSONResponse(status_code=200,content={"message": "Logout successful"})
    except Exception as e:
        return {"message": "Error occurred during logout", "error": str(e)}  

async def password_update(userdata, db:Session, current_user: str):
    try:
        new_password = userdata.new_password

        user = update_password(int(current_user), new_password, db)

        if user is None:
            return JSONResponse(status_code=404,content={"message": "User not found"})

        return JSONResponse(status_code=200,content={"message": "Password updated successfully"})
    except Exception as e:
        return {"message": "Error occurred during password update", "error": str(e)}