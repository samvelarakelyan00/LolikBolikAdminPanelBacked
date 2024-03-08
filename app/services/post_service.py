# Standard libs
# ...

# FastAPI libs
from fastapi import HTTPException, status, Response, Depends
from fastapi.responses import ORJSONResponse

# SqlAlchemy
from sqlalchemy.orm import Session

from schemas.post_schemas import Post
from database import DatabaseConnection, SessionLocal, get_db


session = SessionLocal()


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

        return p

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

        return {"post": post}

    def create_post(self, new_post: Post):
        try:
            self.cursor.execute("""INSERT INTO posts (category_name, content, picture) VALUES (%s, %s, %s) RETURNING*""",
                               (new_post.category_name, new_post.content, new_post.picture))
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

        return {"message": "OK",
                "new_post": new_created_post}

    def delete_post_by_id(self, post_id: int):
        try:
            self.cursor.execute("""DELETE FROM posts
                                    WHERE post_id=%s RETURNING*""",
                                (post_id,))
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error occurred while trying to "
                                       f"delete post by id '{post_id}'\n"
                                       f"ERR: {err}")
        try:
            deleted_post = self.cursor.fetchone()
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error occurred while trying to "
                                       f"fetch deleted post by id '{post_id}'\n"
                                       f"ERR: {err}")

        try:
            self.db_connection.commit()
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error occurred while trying to "
                                       f"commit changes when deleted post by id '{post_id}'\n"
                                       f"ERR: {err}")

        if deleted_post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Post with id '{post_id}' was not found!")

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    def update_post_by_id(self, post_id: int, other_post_data: Post):
        try:
            self.cursor.execute("""UPDATE posts 
                                    SET title=%s, content=%s 
                                    WHERE post_id=%s RETURNING*""",
                                (other_post_data.title, other_post_data.content,
                                 post_id))
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error occurred while trying to "
                                       f"Update post with id '{post_id}'!\n"
                                       f"ERR: {err}")

        try:
            updated_post = self.cursor.fetchone()
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error occurred while trying to "
                                       f"fetch updated post by id '{post_id}'\n"
                                       f"ERR: {err}")

        try:
            self.db_connection.commit()
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error occurred while trying to "
                                       f"commit changes when updated post by id '{post_id}'\n"
                                       f"ERR: {err}")

        if updated_post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Post with id '{post_id}' was not found!")

        return ORJSONResponse(content={
            "message": f"Post with id '{post_id}' successfully updated!",
            "updated_post": updated_post
        })
