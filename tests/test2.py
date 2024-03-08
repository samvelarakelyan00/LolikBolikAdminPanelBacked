image_path = "../app/static/images/xaxavarner/1.jpg"


from PIL import Image

def open_image(image_path):
    try:
        # Open the image file
        image = Image.open(image_path)
        return image
    except FileNotFoundError:
        print("Image file not found.")
        return None
    except Exception as e:
        print(f"Error opening image: {e}")
        return None

# Example usage:
image = open_image(image_path)

if image:
    image.show()  # Show the image using the default image viewer

