from fastapi import FastAPI
from dotenv import load_dotenv
import os   
from model import user_auth
from database_config import engin, get_db,base
from router.admin import router as admin_router
from router.auth import router as auth_router



load_dotenv()

# user_auth.base.metadata.create_all(bind=engin)
app = FastAPI() 
app.include_router(auth_router)
app.include_router(admin_router)

