import os
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, LargeBinary

from database import Base


class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True)
    category_name = Column(String, nullable=False)
    content = Column(String, nullable=False, server_default='')
    picture_path = Column(String, nullable=False, server_default='')
    created_at = Column(DateTime, nullable=False, server_default='now()')
