from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

# Define the directory where your images are stored
IMAGE_DIR = "../app/static/images"


@app.get("/get_image/{category_name}/{image_name}")
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
