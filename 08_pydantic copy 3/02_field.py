from pydantic import BaseModel, Field
from typing import List, Literal

class Employee(BaseModel):
    id: int
    name: str = Field(...,min_length=3, max_length=5, description="Employee name must be between 3 and 5 characters")
    age: int = Field(..., gt=0, lt=100, description="Employee age must be between 0 and 150", )
    salary: float = Field(..., gt=0, description="Employee salary must be greater than 0", example=50000.0) #type: ignore

employee = {"id": 1, "name": "Raj", "age": 30, "salary": 50000.0}
employee_data = Employee(**employee)
print('data:',employee_data)


# decorator

def a(func):
    def wrapper():
        print('a')
        func()
    return wrapper

def b(func):
    def wrapper():
        print('b')
        func()
    return wrapper

@b
@a
def c():
    print('c')

c()