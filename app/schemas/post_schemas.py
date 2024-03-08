from pydantic import BaseModel
from typing import Optional


class Post(BaseModel):
    category_name: str
    content: Optional[str] = ''
    picture: bytes
