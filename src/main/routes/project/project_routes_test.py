import io
import os
import pytest
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

login = {
    "email": "testando@teste.com",
    "password": "@Testando123",
}
data = {
    "name": "Prject",
    "description": "Test" * 20,
    "link_deploy": "https://github.com",
    "link_code": "https://github.com",
}

current_dir = os.path.dirname(__file__)
test_file = os.path.abspath(os.path.join(current_dir, "../../../../test.txt"))


file = None
with open(test_file, "rb") as f:
    file_body = f.read()
    file_object = io.BytesIO(file_body)
    file = ("files", ("test.txt", file_object, "text/plain"))

token = {"Authorization": "Bearer "}


@pytest.mark.asyncio
class TestProjectRoutes:

    async def test_create_project(self):
        login_result = client.post("/login", json=login)
        token["Authorization"] = "Bearer " + login_result.json()["token"]

        response = client.post("/project", files=[file, file], headers=token, data=data)
        print(response.json())
        assert response.status_code == 200
