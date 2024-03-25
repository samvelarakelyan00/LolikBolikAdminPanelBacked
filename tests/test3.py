import requests


resp = requests.get("http://127.0.0.1:8000/posts/get_image/xaxavarner/1.jpg")
print(resp)
print(resp.text)
