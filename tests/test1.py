import requests

# SqlAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, LargeBinary
from PIL import Image
import io

from pydantic import BaseModel
from typing import Optional


class Post(BaseModel):
    category_name: str
    content: Optional[str] = ''
    picture: bytes

# Define your SQLAlchemy model
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost/lolikbolikdb"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class ImageData(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    data = Column(LargeBinary)

# Create a database engine
engine = create_engine('postgresql://postgres:password@localhost/lolikbolikdb')

# Create the tables based on the defined models
# Base.metadata.create_all(engine)

# Create a sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

# Read the image file as binary data
image_path = '../app/static/images/njdeh.jpg'
with open(image_path, 'rb') as f:
    image_binary = f.read()
    print(image_binary)

# Create an instance of the ImageData model
# image = Post(id=1, name='image.jpg', data=image_binary)

# Add the new image instance to the session
# session.add(image)

# Commit the session to save the image data into the database
# session.commit()

# Close the session
# session.close()


# data = {
#     "title": "Garegin Njdeh",
#     "content": "Hzor txa",
#     "image": image
# }
#
#
# url = 'http://127.0.0.1:8000/posts'
# response = requests.post(url, data=data)
#
# print(response.status_code)
