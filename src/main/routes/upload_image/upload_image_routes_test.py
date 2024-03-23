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

current_dir = os.path.dirname(__file__)
test_file = os.path.abspath(os.path.join(current_dir, "../../../../test.txt"))

file_update = None
file = None
with open(test_file, "rb") as f:
    file_body = f.read()
    file_object = io.BytesIO(file_body)
    file = ("files", ("test.txt", file_object, "text/plain"))


@pytest.mark.asyncio
class TestUploadeImageRoutes:

    async def test_upload_imag_unauthorized(self):
        response = client.post(
            "/upload",
            headers={"Authorization": "Bearer "},
            files=[file],
            data={"folder_name": "testing"},
        )
        assert response.status_code == 401
        assert response.json() == {"message": "Invalid token", "type": "unauthorized"}

    async def test_upload_image(self):
        response_token = client.post("/login", json=login)
        token = {"Authorization": f"Bearer {response_token.json()['token']}"}

        response = client.post(
            "/upload",
            headers=token,
            files=[file],
            data={"folder_name": "testing"},
        )

        expected_url = (
            "https://portifolioStaviasz.s3.us-east-005.backblazeb2.com/testing/test"
        )

        assert response.status_code == 200
        assert expected_url in response.json()[0]
