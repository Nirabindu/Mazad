from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import cloudinary


#cloudinary

cloudinary.config(

    cloud_name ="mazadx",
    api_key = "489566656876758",
    api_secret = "4rKl_vgqEPVjnJKBkFPgWQoQdQY"
    )





SQLALCHAMY_DATABASE_URL = (
    "mysql+mysqlconnector://root:admin@localhost:3306/mazad_database"
)


engine = create_engine(SQLALCHAMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
