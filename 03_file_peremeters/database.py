from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base

db_url = "postgresql://postgres:1234@localhost/File"
engine = create_engine(db_url)
session = sessionmaker(bind=engine , autoflush=False , autocommit = False)

Base = declarative_base()

def get_db():
    db = session()

    try:
        yield db
    finally:
        db.close()

        