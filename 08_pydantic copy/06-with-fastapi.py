from operator import ge

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = 'My App'
    admin_email: str = 'raj@example.com'
    items_per_user: int = 10

def get_settings():
    return Settings().model_dump_json()

print(get_settings())