import io
import os
import pytest
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

data = {
    "name": "testando",
    "email": "testando@teste.com",
    "password": "@Testando123",
    "description": "<>description" * 10,
    "contact_description": "<>contact_description" * 10,
}

current_dir = os.path.dirname(__file__)
test_file = os.path.abspath(os.path.join(current_dir, "../../../test.txt"))


file = None
with open(test_file, "rb") as f:
    file_body = f.read()
    file_object = io.BytesIO(file_body)
    file = {"file": ("test.txt", file_object, "text/plain")}

token = {"Authorization": "Bearer "}


@pytest.mark.asyncio
async def test_add_user():
    response = client.post("/user", data=data, files=file)

    body = response.json()
    print(body)
    body_img = body["image_url"]
    del body["image_url"]

    expect_img_url = "https://portifolioStaviasz.s3.us-east-005.backblazeb2.com/users/"

    expect_response = data.copy()
    del expect_response["password"]
    expect_response["id"] = 1

    assert response.status_code == 201
    assert expect_img_url in body_img
    assert expect_response == body
