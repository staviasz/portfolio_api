import pytest

from src.use_case.implements.user.tests.setup import use_case, repository

user = {"id": 1}


@pytest.mark.asyncio
class TestDeleteUserImplementsUseCase:
    async def test_delete_user_implements_use_case_exception(self):
        repository.delete.side_effect = Exception("Error Delete Server")
        response = await use_case.execute(user=user, method="DELETE")

        assert response.status_code == 500
        assert isinstance(response.body["Error"], Exception)
        assert str(response.body["Error"]) == "Error Delete Server"
