import pytest

from src.use_case.implements.user.tests.setup import use_case, data_user, repository


user = data_user.copy()
user["id"] = 1
user["image_url"] = "image_url"
del user["image_upload"]


@pytest.mark.asyncio
class TestGetUserImplementsUseCase:

    async def test_get_user_implements_use_case(self):
        repository.get_by_id_dict.side_effect = lambda **kwargs: user
        result = await use_case.execute(user_id=1, method="GET")

        del user["password"]
        assert result.status_code == 200
        assert result.body == user
