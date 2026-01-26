from fastapi import FastAPI, Request, Depends
from dotenv import load_dotenv
import os   
from model import user_auth
from database_config import engin, get_db,base
from router.admin import router as admin_router
from router.auth import router as auth_router
from sqlalchemy.orm import Session  
from database_config import get_db 
from services.middleware import StoreUserRequestMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from services.middleware import demo_simple_middleware

load_dotenv()

# user_auth.base.metadata.create_all(bind=engin)
app = FastAPI() 



@app.middleware("http")
async def simple_middleware(request: Request, call_next):
    # 🔹 REQUEST MIDDLEWARE
    print("Before endpoint")

    response = await call_next(request)

    # # 🔹 RESPONSE MIDDLEWARE
    # print("After endpoint")
    status = response.status_code
    if status == 500:
        return JSONResponse(content={"details":"Internl server error"}) # For generate error after response and send before client

    return response


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    ip = request.client.host

    # # pseudo code
    # if too_many_requests(ip):
    #     return JSONResponse(
    #         status_code=429,
    #         content={"error": "Too many requests"}
    #     )

    return await call_next(request)

@app.middleware('http')
async def register_middleware(request: Request, call_next):
    return await demo_simple_middleware(request, call_next)


app.add_middleware(StoreUserRequestMiddleware)


app.include_router(auth_router)
app.include_router(admin_router)

