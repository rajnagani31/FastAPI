from pydantic import BaseModel, Field
from typing import List, Literal


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