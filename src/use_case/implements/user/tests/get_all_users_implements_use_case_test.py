import pytest
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.use_case.implements.user.tests.setup import repository, use_case, data_user

user = data_user.copy()
user["image_url"] = "image_url"
user["id"] = 1
del user["image_upload"]


@pytest.mark.asyncio
class TestGetAllUsersImplementsUseCase:
    async def test_get_all_users_exception(self):
        repository.get_all.side_effect = ExceptionCustomPresentation(
            status_code=500, type="Error Server", message="Error GetAll Server"
        )
        response = await use_case.execute()

        assert response.status_code == 500
        assert response.body == {
            "type": "Error Server",
            "message": "Error GetAll Server",
        }

    async def test_get_all_users_success(self):
        repository.get_all.side_effect = lambda *args, **kwargs: [user]
        response = await use_case.execute()

        del user["password"]
        assert response.status_code == 200
        assert response.body == [user]
