from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
db_url = "postgresql+psycopg2://postgres:1234@localhost:5432/model"
engine = create_engine(db_url)
Session = sessionmaker(bind=engine , autoflush=False, autocommit=False) 

Base = declarative_base()
 
def get_db():
    db = Session()
    try:
        return db
    finally:
        db.close()