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
    "link_deploy": "https://github.com/",
    "link_code": "https://github.com/",
}

current_dir = os.path.dirname(__file__)
test_file = os.path.abspath(os.path.join(current_dir, "../../../../test.txt"))

file_update = None
file = None
with open(test_file, "rb") as f:
    file_body = f.read()
    file_object = io.BytesIO(file_body)
    file = ("files", ("test.txt", file_object, "text/plain"))
    file_update = ("files", ("testando.txt", file_object, "text/plain"))

token = {"Authorization": "Bearer "}


@pytest.mark.asyncio
class TestProjectRoutes:

    async def test_create_project(self):
        login_result = client.post("/login", json=login)
        token["Authorization"] = "Bearer " + login_result.json()["token"]

        response = client.post("/project", files=[file, file], headers=token, data=data)

        body = response.json()
        images_body = body["images_urls"]
        del body["images_urls"]

        expect_img_url = (
            "https://portifolioStaviasz.s3.us-east-005.backblazeb2.com/projects/"
        )

        expect_body = data.copy()
        expect_body["id"] = 1

        assert response.status_code == 201
        assert body == expect_body
        assert expect_img_url in images_body[0]
        assert expect_img_url in images_body[1]

    async def test_get_all_projects(self):
        response = client.get("/project")

        expect_img_url = (
            "https://portifolioStaviasz.s3.us-east-005.backblazeb2.com/projects/"
        )

        body_list = response.json()
        assert response.status_code == 200
        assert len(body_list) == 1

        body = body_list[0]
        body_img = body["images_urls"]
        del body["images_urls"]

        expect_body = data.copy()
        expect_body["id"] = 1

        assert body == expect_body
        assert expect_img_url in body_img[0]
        assert expect_img_url in body_img[1]

    async def test_get_project(self):
        response = client.get("/project/1")

        expect_img_url = (
            "https://portifolioStaviasz.s3.us-east-005.backblazeb2.com/projects/"
        )

        body = response.json()
        body_img = body["images_urls"]
        del body["images_urls"]

        expect_body = data.copy()
        expect_body["id"] = 1

        assert response.status_code == 200
        assert body == expect_body
        assert expect_img_url in body_img[0]
        assert expect_img_url in body_img[1]

    async def test_edit_project(self):
        new_data = {"name": "name Update"}
        response = client.put("/project/1", data=new_data, headers=token)

        expect_img_url = (
            "https://portifolioStaviasz.s3.us-east-005.backblazeb2.com/projects/test"
        )

        body = response.json()
        body_img = body["images_urls"]
        del body["images_urls"]

        expect_body = data.copy()
        expect_body["name"] = "name Update"
        expect_body["id"] = 1

        assert response.status_code == 200
        assert body == expect_body
        assert expect_img_url in body_img[0]
        assert expect_img_url in body_img[1]

    async def test_edit_project_whit_files(self):
        response = client.put(
            "/project/1",
            headers=token,
            files=[file_update, file_update],
        )

        expect_img_url = "https://portifolioStaviasz.s3.us-east-005.backblazeb2.com/projects/testando"

        body = response.json()
        body_img = body["images_urls"]
        del body["images_urls"]

        expect_body = data.copy()
        expect_body["name"] = "name Update"
        expect_body["id"] = 1

        assert response.status_code == 200
        assert body == expect_body
        assert expect_img_url in body_img[0]
        assert expect_img_url in body_img[1]

    async def test_delete_project(self):
        response = client.delete("/project/1", headers=token)
        assert response.status_code == 204
        assert response.json() == {}
