import pytest
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.use_case.implements.project.test.setup import use_case, repository, user


@pytest.mark.asyncio
class TestGetAllProjectUseCase:
    async def test_get_all_project_use_case_exception(self):
        repository.get_all.side_effect = ExceptionCustomPresentation(
            status_code=500, type="Error Server", message="Error get all projects"
        )
        response = await use_case.execute(user=user)

        assert response.status_code == 500
        assert response.body == {
            "message": "Error get all projects",
            "type": "Error Server",
        }

    async def test_get_all_project_use_case_success(self):
        repository.get_all.side_effect = lambda *args, **kwargs: []
        response = await use_case.execute(user=user)

        assert response.status_code == 200
        assert isinstance(response.body, list)
