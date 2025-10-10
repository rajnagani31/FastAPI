from sqlalchemy.orm import sessionmaker , declarative_base
from sqlalchemy import create_engine

db_url = "postgresql://postgres:1234@localhost/test"
engine = create_engine(db_url)
session = sessionmaker(bind = engine , autoflush=False)

Base = declarative_base()

def get_db():
    db = session()

    try:
        yield db
    finally:
        db.close()