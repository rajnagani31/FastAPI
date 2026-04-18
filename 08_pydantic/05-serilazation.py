from venv import create
from datetime import datetime   
from pydantic import BaseModel, ConfigDict

# Serialization
class User(BaseModel):
    name: str
    age: int    
    exam_fee: int = 100
    tution_fee: int = 100
    created_at: datetime
    is_active: bool = True

    model_config = ConfigDict(json_encoders={datetime: lambda v: v.strftime('%d-%m-%Y %H:%M:%S')})


data = User(name='Alice', age=23, created_at=datetime(2024, 6, 1, 12, 0, 0))
print(data.model_dump()) # dict-> serialization
print(data.model_dump_json()) # json string -> deserialization