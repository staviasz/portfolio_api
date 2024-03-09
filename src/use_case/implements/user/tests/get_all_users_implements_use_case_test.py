import pytest
from src.use_case.implements.user.tests.setup import repository, use_case, data_user

user = data_user.copy()
user["image_url"] = "image_url"
user["id"] = 1
del user["image_upload"]


@pytest.mark.asyncio
class TestGetAllUsersImplementsUseCase:
    async def test_get_all_users_exception(self):
        repository.get_all.side_effect = Exception("Error GetAll Server")
        response = await use_case.execute(method="GET")

        assert response.status_code == 500
        assert isinstance(response.body["Error"], Exception)
        assert str(response.body["Error"]) == "Error GetAll Server"

    async def test_get_all_users_success(self):
        repository.get_all.side_effect = lambda *args, **kwargs: [user]
        response = await use_case.execute(method="GET")

        del user["password"]
        assert response.status_code == 200
        assert response.body == [user]
