# Standard libraries
# ...

# configs
import configparser

# FastApi
from fastapi import HTTPException

# For Database
# psycopg
import psycopg2
from psycopg2.extras import RealDictCursor


# SqlAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost/lolikbolikdb"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


config = configparser.ConfigParser()
config.read(f'./core/config.ini')

DATABASE_USER = config['DEFAULT']['DATABASE_USER']
DATABASE_HOST = config['DEFAULT']['DATABASE_HOST']
DATABASE_NAME = config['DEFAULT']['DATABASE_NAME']
DATABASE_PASSWORD = config['DEFAULT']['DATABASE_PASSWORD']


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class DatabaseConnection:
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection = cls._instance.__connect()
            cls._instance.cursor = cls._instance.connection.cursor()

        return cls._instance

    def __connect(self):
        if self._connection is not None:
            return self._connection

        try:
            connection = psycopg2.connect(
                user=DATABASE_USER,
                password=DATABASE_PASSWORD,
                host=DATABASE_HOST,
                database=DATABASE_NAME,
                cursor_factory=RealDictCursor
            )
            self._connection = connection
            print("Database Connection Successfully!")
            return connection
        except Exception as e:
            raise HTTPException(status_code=500,
                                detail=f"Database connection error: {e}")

    def get_cursor(self):
        return self.cursor

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()
