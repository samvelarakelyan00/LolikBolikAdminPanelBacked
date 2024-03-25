import requests


url = "http://192.168.1.118:8000/delete-post-by-id/1"

r = requests.delete(url)

print(r.status_code)
# print(r.content)