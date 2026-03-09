import requests

BASE = "http://127.0.0.1:8000/api/notes/"

data = {
    "title": "Test Note",
    "content": "Requests API testing"
}

response = requests.post(BASE, json=data)

assert response.status_code == 200

res = response.json()

assert res["title"] == "Test Note"
assert res["content"] == "Requests API testing"

print("API TEST PASSED")