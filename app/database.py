"""Database setup"""
""" import psycopg2
import time
from psycopg2.extras import RealDictCursor """
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLACHEMY_DATABASE_URL = 'postgresql://fastapi:fastapi@localhost/fastapi'
engine = create_engine(SQLACHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency for controlling db session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


""" while True:
    try:
        conn = psycopg2.connect(host='localhost',
                                database='fastapi',
                                user='fastapi',
                                password='fastapi',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull")
        break
    except psycopg2.DatabaseError as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2) """