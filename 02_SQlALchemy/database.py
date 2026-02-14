from sqlalchemy.orm import sessionmaker , declarative_base
from sqlalchemy import create_engine 

db_url = "postgresql://postgres:1234@localhost/FastAPI"
engin = create_engine(db_url)   
session = sessionmaker(bind = engin, autoflush=False , autocommit = False)


base = declarative_base()


def get_db():
    db = session()

    try:
        yield db
    finally:
        db.close()