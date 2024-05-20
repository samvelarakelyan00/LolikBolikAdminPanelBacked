# Standard libraries
import sys
import os

# FastApi
from fastapi import APIRouter, status, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, ORJSONResponse


# configs
import configparser

config = configparser.ConfigParser()
config.read(f'core/config.ini')

MAIN_DIR = config['DEFAULT']['MAIN_DIR']


# My modules
from .endpoints_support import support
main_path = support.get_main_dir(os.getcwd(), MAIN_DIR)
sys.path.append(main_path)

from schemas import post_schemas
from services import post_service


posts_router = APIRouter()
post_service = post_service.PostService()


IMAGE_DIR = "../app/static/images"

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Max-Age": "3600"

}


@posts_router.delete("/delete-post-by-id/{id}")
def delete_post_by_id(id: int):
    return post_service.delete_post_by_id(id)


@posts_router.get('/get_image/{category_name}/{image_name}')
async def get_image(category_name: str, image_name: str):
    try:
        # Construct the full path to the image
        image_path = f"{IMAGE_DIR}/{category_name}/{image_name}"

        # Return the image file as a response
        return FileResponse(image_path, media_type="image/*", headers=CORS_HEADERS)
    except FileNotFoundError:
        return ORJSONResponse(content={"error": "Image not found"},
                              headers=CORS_HEADERS)
    except Exception as e:
        return ORJSONResponse({"error": str(e)},
                              headers=CORS_HEADERS)


@posts_router.get('')
def f():
    return post_service.get_all_posts()



@posts_router.get("/{id}")
def get_post_by_id(id: int):
    return post_service.get_post_by_id(id)


# Route to handle image upload
@posts_router.post("/uploadpost-by-category/{category_name}")
async def create_upload_post(category_name: str = 'testcategory', file: UploadFile = None):
    try:
        contents = await file.read()
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"ERR: {err}")
    try:
        if os.path.isdir(f"{IMAGE_DIR}/{category_name}"):
            with open(f"{IMAGE_DIR}/{category_name}/{file.filename}", "wb") as f:
                f.write(contents)
        else:
            os.mkdir(f"{IMAGE_DIR}/{category_name}")
            with open(f"{IMAGE_DIR}/{category_name}/{file.filename}", "wb") as f:
                f.write(contents)
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"ERR: {err}")

    pst = post_schemas.Post(category_name=category_name, content='', picture_name=file.filename)

    post_service.create_post(pst)

    return ORJSONResponse(content={'file_name': file.filename},
                          headers=CORS_HEADERS)


@posts_router.get("/by-category/{category_name}")
def get_posts_by_category_name(category_name: str):
    return post_service.get_post_by_category(category_name)
