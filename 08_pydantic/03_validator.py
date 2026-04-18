from turtle import mode

from pydantic import BaseModel, Field, field_validator, model_validator, computed_field


class User(BaseModel):
    """
    Before:
    - Your validation run first
    - Then Pydantic does its validation 

    After:
    - Pydantic does its validation first
    - Then your validation runs

    Wrap:
    - first before your validation runs
    - then Pydantic does its validation -> handler
    - then after your validation runs
    """
    name: str
    age : int = Field(..., ge=18, description='Age must be a positive integer')
    exam_fee: int = 100
    tution_fee: int = 200

    @field_validator('age', mode='after')
    def validate_age(cls, age):
        if age < 0:
            raise ValueError('Age must be a positive integer')
        return age
    
    @model_validator(mode='before')
    def validate_name(cls, values):
        name = values.get('name')
        if not name:
            raise ValueError('Name is required')
        if values.get('age') is not None and 18 > values.get('age'):
            raise ValueError('User must be at least 18 years old')
        return values
    
    @computed_field
    @property
    def total_fee(self) -> int:
        return self.exam_fee + self.tution_fee
    
    @field_validator('exam_fee', mode='wrap')
    def my_validator(cls, value, handler):
        # before
        # if value < 0:
        #     raise ValueError('Exam fee must be a positive integer')
        result = handler(int(value))   # this runs Pydantic validation
        # after
        if result > 500:
            raise ValueError('Exam fee must be less than 500')
        return result
    
data = User(name='Alice', age=23, exam_fee=100, tution_fee=100)
print(data.total_fee)
print(data.model_dump())
print(data.model_dump_json())
print(data)

from pydantic import BaseModel, field_validator

class User_data(BaseModel):
    age: int

    @field_validator('age', mode='before')
    def convert_age(cls, value):
        print("Before:", value)
        return int(value)  # convert string → int
    
print(User_data(age='30'))


from typing import Annotated

from pydantic import AfterValidator, BaseModel


def is_even(value: int) -> int:
  if value % 2 == 1:
      raise ValueError(f'{value} is not an even number')
  return value


EvenNumber = Annotated[int, AfterValidator(is_even)]


class Model1(BaseModel):
  my_number: EvenNumber


class Model2(BaseModel):
  other_number: Annotated[EvenNumber, AfterValidator(lambda v: v + 2)]


class Model3(BaseModel):
  list_of_even_numbers: list[EvenNumber]  

class Model4(BaseModel):
   num : int

   @field_validator('num', mode='after')
   def add_two(cls, value):
       return value + 2 
   
print(Model1(my_number=4))
print(Model2(other_number=4))
print(Model4(num='5'))


from pydantic_core import PydanticCustomError

from pydantic import BaseModel, ValidationError, field_validator


class Model(BaseModel):
    x: int

    @field_validator('x', mode='after')
    @classmethod
    def validate_x(cls, v: int) -> int:
        if v % 42 == 0:
            raise PydanticCustomError(
                'the_answer_error',
                '{number} is the answer!',
                {'number': v},
            )
        return v


try:
    Model(x=42 * 2)
except ValidationError as e:
    print(e)
    """
    1 validation error for Model
    x
      84 is the answer! [type=the_answer_error, input_value=84, input_type=int]
    """

