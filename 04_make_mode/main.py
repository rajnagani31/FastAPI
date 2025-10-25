from database import Base, engine
from model.user import *
from fastapi import FastAPI
from model.admin import Admin
# Register the Table with metadata
user()
store()
incidents()
suspectsimages()
liked_incidents()
witness_statements()
video()
category()
policemaster()
cases()
casestatus()
suspects()
example()
# Create the table(s) in the connected database
Base.metadata.create_all(bind=engine)
Admin.__table__.create(bind=engine, checkfirst=True)
app = FastAPI()


print("Tables created (if not already present).")

