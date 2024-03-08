# Standard libraries
# ...

# FastApi libraries
from fastapi import FastAPI

# Connection to db
from database import DatabaseConnection, engine

db_connection = DatabaseConnection()
cursor = db_connection.get_cursor()

# My modules
# from api import posts_api_router, users_api_router
from api import posts_api_router
from models import post_models

post_models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def main():
    return {"message": "Hello, world!"}


app.include_router(posts_api_router)
