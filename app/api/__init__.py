# app/api/__init__.py
import os
import sys
# configs
import configparser

config = configparser.ConfigParser()
config.read(f'core/config.ini')

MAIN_DIR = config['DEFAULT']['MAIN_DIR']


# My modules
from .endpoints.endpoints_support import support
main_path = support.get_main_dir(os.getcwd(), MAIN_DIR)
sys.path.append(main_path)

from fastapi import APIRouter

from .endpoints import post_endpoints, admin_endpoints

# posts
posts_api_router = APIRouter()
posts_api_router.include_router(post_endpoints.posts_router, prefix="/posts", tags=["posts"])


# admin
# users_api_router = APIRouter()
# users_api_router.include_router(admin_endpoints.admin_router, prefix="/admin", tags=["admin"])
