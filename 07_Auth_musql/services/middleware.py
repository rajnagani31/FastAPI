from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from model.user_auth import UserAuth,UserToken
import logging
from fastapi.responses import Response,JSONResponse
import hashlib
from fastapi.responses import JSONResponse
from fastapi import status, Request
from model.loog import ServerLogs
from database_config import get_db
from starlette.middleware.base import BaseHTTPMiddleware
from dotenv import load_dotenv
import os,jwt
from starlette.requests import Request as StarletteRequest
from starlette.concurrency import iterate_in_threadpool

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

class StoreUserRequestMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        print("run middleware No 4")
        db: Session = next(get_db())

        # Headers
        token = request.headers.get("Authorization")
        session_id = request.cookies.get("session")
        user_id = None
        if token:
            payload = jwt.decode(
                token.replace("Bearer ", ""),
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )
            user_id = payload.get("sub")

        body = await request.body()


        #     # IMPORTANT: re-inject request body
        # async def receive():
        #         return {"type": "http.request", "body": body}
        # request = StarletteRequest(request.scope, receive)

        # response = await call_next(request)

        # response_body = b""
        # async for chunk in iterate_in_threadpool(response.body_iterator):
        #     response_body += chunk

        # # Restore response body
        # response.body_iterator = iter([response_body])

        try:
            # log DB save process
            log = ServerLogs(
                user_id = user_id,
                session_id = session_id,
                user_ip = request.client.host,
                api_method=request.method,
                url=str(request.url),
                payload=body if body else None, #.decode("utf-8")
                token=token,
                # response=response_body.decode("utf-8")
            )
            db.add(log)
            db.commit()

        

            response = await call_next(request) # send request to api endpoint thet wait for a response

            print("After endpoint No 4")
            status = response.status_code
            print("status no 4",status)
            if status == 500:
                return JSONResponse(content={"details":"Access forbidden: Admins only"}) # For generate error after response and send before client
            return response
        except Exception as e:
                db.rollback()
                print("Middleware error:", e)


async def demo_simple_middleware(request: Request, call_next):
    print("Before endpoint NO 3")
    response = await call_next(request)
    print("After endpoint :3")
    return response