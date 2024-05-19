import pytest
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

login = {
    "email": "testando@teste.com",
    "password": "@Testando123",
}
data = {
    "html": "<h1>Testando</h1>" * 20,
    "images_urls": ["https://i.ibb.co/2Jn8w8j.com/testando.jpg"],
    "name": "post test",
}

token = {"Authorization": "Bearer "}


@pytest.mark.asyncio
class TestPostRoutes:
    async def test_create_post(self):
        response = client.post("/login", json=login)
        token["Authorization"] = "Bearer " + response.json()["token"]
        response = client.post("/post", headers=token, json=data)
        print(response.json())

        assert response.status_code == 201
        assert response.json() == {
            "id": 1,
            "html": data["html"],
            "user_id": 1,
            "name": data["name"],
            "images_urls": data["images_urls"],
        }

    async def test_update_post(self):
        data["html"] = "<h1>Testando Update</h1>" * 20

        response = client.put("/post/1", headers=token, json=data)

        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "html": data["html"],
            "user_id": 1,
            "name": data["name"],
            "images_urls": data["images_urls"],
        }

    async def test_get_post(self):
        response = client.get("/post/1")

        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "html": data["html"],
            "user_id": 1,
            "name": data["name"],
            "images_urls": data["images_urls"],
        }

    async def test_get_all_posts(self):
        response = client.get("/post")

        assert response.status_code == 200
        assert response.json() == [
            {
                "id": 1,
                "html": data["html"],
                "user_id": 1,
                "name": data["name"],
                "images_urls": data["images_urls"],
            },
        ]

    async def test_get_all_posts_with_wrong_filter(self):
        response = client.get("/post?user_id=2")

        assert response.status_code == 200
        assert response.json() == []

    async def test_delete_post(self):
        response = client.delete("/post/1", headers=token)

        assert response.status_code == 204
        assert response.json() == {}
