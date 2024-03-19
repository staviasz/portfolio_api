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
test_file = os.path.abspath(os.path.join(current_dir, "../../../../test.txt"))


file = None
with open(test_file, "rb") as f:
    file_body = f.read()
    file_object = io.BytesIO(file_body)
    file = {"file": ("test.txt", file_object, "text/plain")}

token = {"Authorization": "Bearer "}


@pytest.mark.asyncio
class TestUserRoutes:

    async def test_login(self):
        login_data = {
            "email": data["email"],
            "password": data["password"],
        }
        response = client.post("/login", json=login_data)

        token["Authorization"] = "Bearer " + response.json()["token"]

        assert response.status_code == 200
        assert token

    async def test_update_anauthorized(self):

        response = client.put(
            "/user", data=data, headers={"Authorization": "Bearer token"}
        )

        assert response.status_code == 401
        assert response.json() == {
            "Error": {
                "status_code": 401,
                "type": "UnauthorizedException",
                "message": "invalid access credentials",
            }
        }

    async def test_update_success(self):
        new_data = data.copy()
        new_data["name"] = "name Update"
        response = client.put("/user", data=new_data, headers=token)

        expect_img_url = (
            "https://portifolioStaviasz.s3.us-east-005.backblazeb2.com/users/"
        )

        body = response.json()
        body_img = body["image_url"]
        del body["image_url"]

        del new_data["password"]
        new_data["id"] = 1

        assert response.status_code == 200
        assert expect_img_url in body_img
        assert new_data == body

    async def test_get_user(self):
        response = client.get("/user/profile", headers=token)

        expect_img_url = (
            "https://portifolioStaviasz.s3.us-east-005.backblazeb2.com/users/"
        )

        except_response = data.copy()
        body = response.json()
        body_img = body["image_url"]
        del body["image_url"]

        del except_response["password"]
        except_response["id"] = 1

        assert response.status_code == 200
        assert expect_img_url in body_img
        assert except_response == body

    # async def test_get_all_user(self):
    #     response = client.get("/user", headers=token)

    #     body = response.json()
    #     assert isinstance(body, list)

    #     expect_img_url = (
    #         "https://portifolioStaviasz.s3.us-east-005.backblazeb2.com/users/"
    #     )

    #     body_dict = body[0]
    #     body_img = body_dict["image_url"]
    #     del body_dict["image_url"]

    #     except_response = {
    #         "id": 1,
    #         "name": "name Update",
    #         "email": "testando@teste.com",
    #         "description": "<>description" * 10,
    #         "contact_description": "<>contact_description" * 10,
    #     }

    #     assert response.status_code == 200
    #     assert expect_img_url in body_img
    #     assert body_dict == except_response

    async def test_delete_user(self):
        response = client.delete("/user", headers=token)
        assert response.status_code == 204
        assert response.json() == {}
