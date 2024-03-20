import pytest
from src.use_case.implements.project.test.setup import use_case, repository, user


@pytest.mark.asyncio
class TestDeleteProjectUseCase:
    async def test_delete_project_use_case_exception(self):
        repository.delete_with_related.side_effect = Exception("Error Delete Server")
        response = await use_case.execute(project_id=1, method="DELETE", user=user)

        assert response.status_code == 500
        assert isinstance(response.body["Error"], Exception)
        assert str(response.body["Error"]) == "Error Delete Server"

    async def test_delete_project_use_case_success(self):
        repository.delete_with_related.side_effect = lambda *args, **kwargs: None
        response = await use_case.execute(project_id=1, method="DELETE", user=user)

        assert response.status_code == 204
        assert response.body == {}
