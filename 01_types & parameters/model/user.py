from sqlalchemy import Column ,Integer ,String ,Boolean
from database.database_confige import Base

class Login(Base):
    __tablename__ = "user_details"

    user_id = Column(Integer ,primary_key=True , index=True)
    user_name = Column(String(50) , nullable= True)
    password = Column(String(8) , nullable=True)

    

