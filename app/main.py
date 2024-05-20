# Standard libraries
# ...

# FastApi libraries
from fastapi import FastAPI, Response, status, Request, HTTPException
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

# Connection to db
from database import DatabaseConnection, engine

db_connection = DatabaseConnection()
cursor = db_connection.get_cursor()

# My modules
# from api import posts_api_router, users_api_router
from api import posts_api_router
from models import post_models, admin_models

post_models.Base.metadata.create_all(bind=engine)
admin_models.Base.metadata.create_all(bind=engine)

from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware


app = FastAPI(middleware=[
    Middleware(CORSMiddleware, allow_origins=["*"],allow_methods=["*"])
])


origins = [

    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
    "http://192.168.1.118:8000",
    "http://192.168.1.118",
    "http://192.168.5.86:8000",
    "http://192.168.5.86",
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://192.168.122.167:8000",
    "http://192.168.122.167",
]

app.add_middleware(
    # CORSMiddleware,
    # allow_origins=origins,
    # allow_credentials=True,
    # allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    # allow_headers=["Authorization", "Content-Type", "Accept"],
    # expose_headers=["Content-Disposition"],
CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from fastapi.responses import HTMLResponse, FileResponse


@app.get("/", response_class=HTMLResponse)
def main():
    # return {"message": "Hello, world!"}
    return FileResponse(path="../tests/posttoserver/index.html")


from services import post_service


@app.get("/delete-post-by-id/{post_id}")
def delete_post_by_id(post_id: int):
    CORS_HEADERS = {
        "Access-Control-Allow-Origin": "*",
        "Accept-Control--Allow-Origin": "*",
        "Access-Control-Allow-Methods": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Max-Age": "3600",
    }
    try:
        cursor.execute("""DELETE FROM posts
                                WHERE post_id=%s RETURNING*""",
                            (str(post_id),))
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error occurred while trying to "
                                   f"delete post by id '{post_id}'\n"
                                   f"ERR: {err}",
                            headers=CORS_HEADERS)
    # try:
    #     deleted_post = cursor.fetchone()
    # except Exception as err:
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #                         detail="Error occurred while trying to "
    #                                f"fetch deleted post by id '{post_id}'\n"
    #                                f"ERR: {err}",
    #                         headers=CORS_HEADERS)

    try:
        db_connection.commit()
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error occurred while trying to "
                                   f"commit changes when deleted post by id '{post_id}'\n"
                                   f"ERR: {err}",
                            headers=CORS_HEADERS)

    # if deleted_post is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Post with id '{post_id}' was not found!",
    #                         headers=CORS_HEADERS)

    return ORJSONResponse(content={"message": "delete was successful!"},
                          headers=CORS_HEADERS)


app.include_router(posts_api_router)

#
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)
