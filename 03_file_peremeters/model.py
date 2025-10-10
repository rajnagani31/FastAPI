from sqlalchemy import Column , ForeignKey , Integer ,String ,Boolean , DateTime , BigInteger , LargeBinary , func
from database import Base

class User_details(Base):
    __tablename__ = "user data"

    id = Column(Integer,primary_key=True)
    user_name = Column("user_name", String(50))
    created_at = Column("created_at" , DateTime(timezone=True) , server_default = func.now() ,nullable = True)
    updated_at = Column(DateTime(timezone=True) , server_default = func.now() ,nullable =True)

class User_file_data(Base):
    __tablename__ = "File data"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("user data.id"), nullable=False)
    file_name = Column(String(255), nullable=True)
    file_type = Column(String(255), nullable=True)
    file_size = Column(Integer, nullable=True)
    size_readable = Column(String(32), nullable=True)
    file_data = Column(LargeBinary, nullable=True)
