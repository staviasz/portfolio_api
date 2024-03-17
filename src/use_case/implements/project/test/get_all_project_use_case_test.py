import pytest
from src.use_case.implements.project.test.setup import use_case, repository


@pytest.mark.asyncio
class TestGetAllProjectUseCase:
    async def test_get_all_project_use_case_exception(self):
        repository.get_all.side_effect = Exception("Error get all projects")
        response = await use_case.execute()

        assert response.status_code == 500
        assert isinstance(response.body["Error"], Exception)
        assert str(response.body["Error"]) == "Error get all projects"

    async def test_get_all_project_use_case_success(self):
        repository.get_all.side_effect = lambda *args, **kwargs: []
        response = await use_case.execute()

        assert response.status_code == 200
        assert isinstance(response.body, list)
