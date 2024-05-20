# Standard libs
import os

# FastAPI libs
from fastapi import HTTPException, status, Response, Request, UploadFile
from fastapi.responses import ORJSONResponse

# SqlAlchemy
from sqlalchemy.orm import Session

from schemas.post_schemas import Post
from database import DatabaseConnection, SessionLocal, get_db


session = SessionLocal()

IMAGE_DIR = f"{os.getcwd()}/images"

# CORS_HEADERS = {
#     "Access-Control-Allow-Origin": "*",
#     "Access-Control-Allow-Credentials": "true"
# }

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Max-Age": "3600"

}


class PostService:
    def __init__(self):
        self.db_connection = DatabaseConnection()
        self.cursor = self.db_connection.get_cursor()

    def get_all_posts(self):
        try:
            self.cursor.execute("""SELECT * FROM posts""")
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error occurred while trying to "
                                       "get all posts!\n"
                                       f"ERR: {err}")
        try:
            p = self.cursor.fetchall()
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error occurred while trying to "
                                       "fetch all posts!\n"
                                       f"ERR: {err}")

        return ORJSONResponse({"all_posts": p},
                              headers=CORS_HEADERS)

    def upload_post(self, category_name: str, file: UploadFile):
        print(os.getcwd())
        contents = file.read()
        try:
            with open(f"{IMAGE_DIR}/{category_name}/{file.filename}", "wb") as f:
                f.write(contents)
        except Exception as err:
            print(err)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Error")

        return ORJSONResponse({"filename": file.filename},
                              headers=CORS_HEADERS)

    def get_post_by_id(self, post_id):
        try:
            self.cursor.execute("""SELECT * FROM posts
                                    WHERE post_id=%s""",
                                (post_id,))
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error occurred while trying to "
                                       f"get post by id '{post_id}'\n"
                                       f"ERR: {err}")
        try:
            post = self.cursor.fetchone()
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error occurred while trying to "
                                       f"fetch the post got by id '{post_id}'\n"
                                       f"ERR: {err}")
        if post is None:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                 detail=f"Post with id '{post_id}' was not found!")

        return ORJSONResponse({"post": post},
                              headers=CORS_HEADERS)

    def create_post(self, new_post: Post):
        try:
            self.cursor.execute("""SELECT picture_name FROM posts""")
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error occurred while trying to "
                                       "select all pictures names!\n"
                                       f"ERR: {err}")
        try:
            all_pictures_names = self.cursor.fetchall()
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error occurred while trying to "
                                       "fetch all pictures names!\n"
                                       f"ERR: {err}")
        # TODO
        try:
            self.cursor.execute("""INSERT INTO posts (category_name, content, picture_name) VALUES (%s, %s, %s) RETURNING*""",
                               (new_post.category_name, new_post.content, new_post.picture_name))
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error occurred while trying to "
                                       "create new post!\n"
                                       f"ERR: {err}")
        try:
            new_created_post = self.cursor.fetchone()
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error occurred while trying to "
                                       "fetch new created post!\n"
                                       f"ERR: {err}")
        try:
            self.db_connection.commit()
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error occurred while trying to "
                                       "commit changes into database when created new post!\n"
                                       f"ERR: {err}")

        return ORJSONResponse({"message": "OK",
                               "new_post": new_created_post},
                              headers=CORS_HEADERS)

    def delete_post_by_id(self, post_id: int, request: Request):
        print(request.headers)
        print(request.url)
        try:
            self.cursor.execute("""DELETE FROM posts
                                    WHERE post_id=%s RETURNING*""",
                                (post_id,))
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error occurred while trying to "
                                       f"delete post by id '{post_id}'\n"
                                       f"ERR: {err}",
                                headers=CORS_HEADERS)
        try:
            deleted_post = self.cursor.fetchone()
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error occurred while trying to "
                                       f"fetch deleted post by id '{post_id}'\n"
                                       f"ERR: {err}",
                                headers=CORS_HEADERS)

        try:
            self.db_connection.commit()
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error occurred while trying to "
                                       f"commit changes when deleted post by id '{post_id}'\n"
                                       f"ERR: {err}",
                                headers=CORS_HEADERS)

        if deleted_post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Post with id '{post_id}' was not found!",
                                headers=CORS_HEADERS)

        return ORJSONResponse(content={'message': "deletion was successful!"},
                        headers=CORS_HEADERS)

    def get_post_by_category(self, category_name: str):
        try:
            self.cursor.execute("""SELECT * FROM posts
                                    WHERE category_name=%s""",
                                (category_name,))
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error occurred while trying to "
                                       f"Update post with category '{category_name}'!\n"
                                       f"ERR: {err}")

        try:
            posts = self.cursor.fetchall()
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error occurred while trying to "
                                       f"fetch get posts by category '{category_name}'\n"
                                       f"ERR: {err}")

        try:
            self.db_connection.commit()
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error occurred while trying to "
                                       f"commit changes when get posts by category '{category_name}'\n"
                                       f"ERR: {err}")

        if len(posts) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Post with category '{category_name}' was not found!")

        return ORJSONResponse(content={
            "posts": posts
        }, headers=CORS_HEADERS)
