

from config import config
import datetime
from jose import jwt
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm,HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from database import new_validate_token_table,database
from jwt import ExpiredSignatureError, InvalidTokenError


bearer_scheme = HTTPBearer()
SECRET_KEY = config.SECRET_KEY
ALGORITHM = "HS256"


def access_token(user_id : int):
    expire = datetime.datetime.now(datetime.timezone.utc) + timedelta(days=1)
    jwt_data = {
        'sub': str(user_id),
        'exp': expire,
        "type": "access"
    }
    encoded_jwt = jwt.encode(jwt_data , SECRET_KEY, algorithm = ALGORITHM)

    return encoded_jwt

def refresh_token(user_id : int):
    expire = datetime.datetime.now(datetime.timezone.utc) + timedelta(days=1)
    jwt_data = {
        "sub":user_id,
        "exp":expire,
        "type":"refresh"
    }
    encoded_jwt = jwt.encode(jwt_data,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id: str = payload.get("sub")
        query = new_validate_token_table.select().where(new_validate_token_table.c.token == token)
        result = await database.fetch_one(query)

        if not result or result['is_deleted']:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token or token has been revoked",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_id
    
    except (InvalidTokenError, ExpiredSignatureError,IndexError,ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )