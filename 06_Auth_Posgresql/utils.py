

from config import config
import datetime
from jose import jwt
from datetime import timedelta

SECRET_KEY = config.SECRET_KEY
ALGORITHM = "HS256"


def access_token(user_id : int):
    expire = datetime.datetime.now(datetime.timezone.utc) + timedelta(days=1)
    jwt_data = {
        'sub': user_id,
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