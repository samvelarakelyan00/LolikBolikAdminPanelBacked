# Standard libraries
import sys
import os

# FastApi
from fastapi import APIRouter, status
from fastapi.responses import FileResponse


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


@posts_router.get('/get_image/{category_name}/{image_name}')
async def get_image(category_name: str, image_name: str):
    try:
        # Construct the full path to the image
        image_path = f"{IMAGE_DIR}/{category_name}/{image_name}"

        # Return the image file as a response
        return FileResponse(image_path, media_type="image/*")
    except FileNotFoundError:
        return {"error": "Image not found"}
    except Exception as e:
        return {"error": str(e)}


@posts_router.get('')
def f():
    return post_service.get_all_posts()


@posts_router.post('')
def insert_post(new_post: post_schemas.Post):
    return post_service.create_post(new_post)


@posts_router.get("/{id}")
def get_post_by_id(id: int):
    return post_service.get_post_by_id(id)


@posts_router.delete("/{id}")
def delete_post_by_id(id: int):
    return post_service.delete_post_by_id(id)


@posts_router.put("/{id}")
def update_post_by_id(id: int, other_post_data: post_schemas.Post):
    return post_service.update_post_by_id(id, other_post_data)
