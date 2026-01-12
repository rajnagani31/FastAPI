import sqlalchemy
import databases

from model.user import user_register , validate_token, student_details , course_details,markes_details
from sqlalchemy.engine.url import make_url
from sqlalchemy_utils import database_exists, create_database
from config import config   




metadata =sqlalchemy.MetaData()

user_details_table = user_register(metadata)
user_jwt_token_table = validate_token(metadata)
student_details_table = student_details(metadata)
course_details_table = course_details(metadata) 
markes_details_table = markes_details(metadata)


url = make_url(config.DB_URL)
if not database_exists(url):
    print(f"⚙️ Database does not exist. Creating: {url.database}")
    create_database(url)
else:
    print(f"✅ Database already exists: {url.database}")

db_args = {"min_size": 1, "max_size": 3} if "postgres" in config.DB_URL else {}

# database = databases.Database(os.getenv("DB_URL"))
database = databases.Database(config.DB_URL , force_rollback=config.FORCE_ROLLBACK , **db_args)
engine = sqlalchemy.create_engine(
    config.DB_URL
)
metadata.create_all(engine)
print("✅ Tables created successfully.")
print(config.DB_URL)
print(config.USER)
