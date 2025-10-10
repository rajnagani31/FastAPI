from pydantic import BaseModel

class user_login(BaseModel):
    user_name : str | None = None
    password : str | None = None

