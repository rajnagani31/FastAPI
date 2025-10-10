from sqlalchemy import Column , Integer ,String ,Boolean
from database import base


class User(base):
    __tablename__ = "user"

    id = Column(Integer , primary_key=True , index=True)
    email = Column(String(100) , nullable=True)
    name = Column(String(50) ,nullable=False , index = True)
    age = Column(Integer, nullable=True)
    is_active = Column(Boolean , nullable=True)
    is_rescane = Column(Boolean , nullable=True)
    isinstance = Column(Boolean ,nullable=True)
    ok= Column(Boolean ,nullable=True)
    new = Column(Integer , nullable=True)
    new_new = Column(Integer , nullable=True)

    

class Phone(base):
    __tablename__ = "phone"

    id = Column(Integer , primary_key=True , index=True)
    email = Column(String(100) , nullable=True)
    name = Column(String(50) ,nullable=False , index = True)
    age = Column(Integer, nullable=True)
    is_active = Column(Boolean , nullable=True)
    new_new = Column(Integer , nullable=True)


