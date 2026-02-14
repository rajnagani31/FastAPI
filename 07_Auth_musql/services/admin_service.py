from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from model.user_auth import UserAuth,UserToken
import logging
import hashlib
from fastapi.responses import JSONResponse
from fastapi import status



def all_user(db: Session):
    try:
        # users = db.query(UserAuth).all()

        users = (db.query(UserAuth, UserToken).join(UserAuth, UserAuth.id == UserToken.user_id).all())
        if users:
            user_list = [
                {
                    "id": user_auth
                }
                for user_auth, user_token in users
            ]
            return user_list
        else:
            return None
    except Exception as e:
        logging.error(f"Error retrieving users: {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Internal server error"})
    


def get_user(db:Session,user_id = None,token=None):
    user = db.query(UserAuth).filter(UserAuth.id == user_id).first()

    print(user)
    print(user_id)
    print(token)
    if token:
        user = db.query(UserToken).filter(UserToken.token == token).first()
        return user.user_id
    else:
        return user.id
    
