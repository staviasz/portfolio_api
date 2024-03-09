import pytest
from src.domain.models.user_models_domain import UserModelCreateDomain

from src.use_case.implements.user.tests.setup import (
    use_case,
    data_user,
    repository,
    bucket,
)

data_add_user = UserModelCreateDomain(**data_user)


@pytest.mark.asyncio
class TestAddUserImplementsUseCase:
    async def test_get_by_email_exception(self):
        repository.get_by_email.side_effect = Exception("Error Email Server")
        response = await use_case.execute(data_user=data_add_user)

        assert response.status_code == 500
        assert isinstance(response.body["Error"], Exception)
        assert str(response.body["Error"]) == "Error Email Server"

    async def test_get_by_email_exists(self):
        repository.get_by_email.side_effect = lambda *args, **kwargs: True
        response = await use_case.execute(data_user=data_add_user)

        assert response.status_code == 409
        assert response.body["message"] == "Email already exists"

    async def test_get_by_email_success(self):
        new_user = data_user.copy()
        new_user["id"] = 1
        new_user["image_url"] = "image_url"
        del new_user["image_upload"]

        repository.get_by_email.side_effect = lambda *args, **kwargs: None
        repository.create.side_effect = lambda *args, **kwargs: new_user
        response = await use_case.execute(data_user=data_add_user)

        del new_user["password"]
        assert response.status_code == 201
        assert response.body == new_user

    async def test_upload_exception(self):
        bucket.upload.side_effect = Exception("Error Upload Server")
        response = await use_case.execute(data_user=data_add_user)

        assert response.status_code == 500
        assert isinstance(response.body["Error"], Exception)
        assert str(response.body["Error"]) == "Error Upload Server"

    async def test_upload_success(self):
        new_user = data_user.copy()
        new_user["id"] = 1
        new_user["image_url"] = "image_url"
        del new_user["image_upload"]

        bucket.upload.side_effect = lambda *args, **kwargs: "image_url"
        repository.create.side_effect = lambda *args, **kwargs: new_user
        response = await use_case.execute(data_user=data_add_user)

        del new_user["password"]
        assert response.status_code == 201
        assert response.body == new_user

    async def test_create_exception(self):
        repository.create.side_effect = Exception("Error Create Server")
        response = await use_case.execute(data_user=data_add_user)

        assert response.status_code == 500
        assert isinstance(response.body["Error"], Exception)
        assert str(response.body["Error"]) == "Error Create Server"
