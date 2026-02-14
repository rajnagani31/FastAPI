from sqlalchemy.orm import Session
from services.user_service import create_user,get_user_by_email,insert_token,update_password,logout_user
from fastapi import HTTPException,status, Depends
from fastapi.responses import JSONResponse
from dependencies import verify_token,access_token,refresh_token
import hashlib
from services.admin_service import all_user
import logging

logger = logging.getLogger(__name__)




async def get_all_user(db: Session):
    try:
        data = all_user(db)

        if data is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No users found"})
        
        return data
    except Exception as e:
        logger.error(f"Error retrieving users: {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Internal server error"})