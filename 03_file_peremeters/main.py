from routes import routrs as user_file
from database import Base ,get_db ,engine
import model
from fastapi import FastAPI

model.Base.metadata.create_all(bind = engine)

app = FastAPI()
app.include_router(user_file)