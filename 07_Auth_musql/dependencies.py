from jose import JWTError, jwt  
from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status, Request
from model.user_auth import UserToken,UserAuth
from dotenv import load_dotenv
import os
from typing import Annotated
from datetime import timedelta
import datetime
from sqlalchemy.orm import Session
from database_config import get_db
import time
load_dotenv()

bearer_scheme = HTTPBearer()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


def create_credentials_exception(detail: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )

def access_token(user_id: int):
    expire = datetime.datetime.now(datetime.timezone.utc) + timedelta(days=1)
    jwt_data = {
        'sub': str(user_id),
        'exp': expire,
        "type": "access"
    }
    encoded_jwt = jwt.encode(jwt_data, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def refresh_token(user_id:int):
    expire = datetime.datetime.now(datetime.timezone.utc) + timedelta(days=1)
    jwt_data = {
        "sub":user_id,
        "exp":expire,
        "type":"refresh"
    }
    encoded_jwt = jwt.encode(jwt_data,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt

async def verify_token(request : Request,credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),db:Annotated[Session, Depends(get_db)] = None):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        print("Payload:", payload)
        user_id: str = payload.get("sub")
        # ORM query to validate token can be added here
        start = time.time()
        query = db.query(UserToken).filter(UserToken.user_id == int(user_id)).first()
        user = db.query(UserAuth).filter(UserAuth.id == int(user_id)).first()
        end = time.time()

        print("DB Time:",end-start)

        user_role = user.user_role if user else None
        print("User Role:", user_role)
        if query is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token or user does not exist",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if query.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User is deleted",
                headers={"WWW-Authenticate": "Bearer"},
            )
        request.state.user_id = user_id
        request.user_role = user_role
        return user_id
    
    except (InvalidTokenError, ExpiredSignatureError,IndexError,ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    

def decode_refresh_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError as e:
        raise create_credentials_exception("Refresh token has expired") from e
    except InvalidTokenError as e:
        raise create_credentials_exception("teInvalid refresh token") from e
    