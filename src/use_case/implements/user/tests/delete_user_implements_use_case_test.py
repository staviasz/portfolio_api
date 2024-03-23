import pytest

from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.use_case.implements.user.tests.setup import use_case, repository

user = {"id": 1}


@pytest.mark.asyncio
class TestDeleteUserImplementsUseCase:
    async def test_delete_user_implements_use_case_exception(self):
        repository.delete.side_effect = ExceptionCustomPresentation(
            status_code=500, type="Error Server", message="Error Delete Server"
        )
        response = await use_case.execute(user=user, method="DELETE")

        assert response.status_code == 500
        assert response.body == {
            "message": "Error Delete Server",
            "type": "Error Server",
        }
