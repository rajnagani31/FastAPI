from functools import wraps
from pydantic import BaseModel, Field


class Employee(BaseModel):
    id: int
    name: str = Field(
        ...,
        min_length=3,
        max_length=5,
        description="Employee name must be between 3 and 5 characters",
    )
    age: int = Field(
        ...,
        gt=0,
        lt=100,
        description="Employee age must be between 0 and 100",
    )
    salary: float = Field(
        ...,
        gt=0,
        description="Employee salary must be greater than 0",
        examples=[50000.0],
    )


employee = {"id": 1, "name": "Raj", "age": 30, "salary": 50000.0}
employee_data = Employee(**employee)
print("data:", employee_data)


# decorator


def a(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("a")
        return func(*args, **kwargs)

    return wrapper


def b(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("b")
        return func(*args, **kwargs)

    return wrapper


@b
@a
def c():
    print("c")


c()