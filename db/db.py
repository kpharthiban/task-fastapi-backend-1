from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Setting the URL/Location of the database
URL_DATABASE = "sqlite:///./db/items.db"

# Creating a single engine object for code to connect to database
engine = create_engine(URL_DATABASE, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Creating database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()