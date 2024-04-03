import pytest
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.use_case.implements.post.tests.setup import repository, use_case, data, user


@pytest.mark.asyncio
class TestGetAllPostUseCase:
    async def test_get_all_post_exception(self):
        repository.get_all.side_effect = ExceptionCustomPresentation(
            status_code=500, type="Error Server", message="Error GetAll Server"
        )
        response = await use_case.execute(user=user, method="GET")

        assert response.status_code == 500
        assert response.body == {
            "type": "Error Server",
            "message": "Error GetAll Server",
        }

    async def test_get_all_post_success(self):
        repository.get_all.side_effect = lambda *args, **kwargs: [
            {**data, "user_id": 1}
        ]
        response = await use_case.execute(user=user, method="GET")
        assert response.status_code == 200
        assert response.body == [{**data, "user_id": 1}]
