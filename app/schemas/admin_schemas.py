from pydantic import BaseModel
from typing import Optional


class AdminCreate(BaseModel):
    name: str
    surname: str
    email: str
    password: str
