#  This file contains the database connection and session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#  This is the database URL. It is a relative path to the database file.
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

#  This is the database engine. It is used to connect to the database.
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
#  This is the database session. It is used to interact with the database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#  This is the base class for the database model.
Base = declarative_base()


#  This function is used to get the database session.
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


