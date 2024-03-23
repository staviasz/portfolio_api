import pytest
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.use_case.implements.project.test.setup import repository, use_case, data, user


@pytest.mark.asyncio
class TestGetProjectUseCase:
    async def test_get_project_use_case_exception(self):
        repository.get_by_id_dict.side_effect = ExceptionCustomPresentation(
            status_code=500, type="Error Server", message="Error Repository Server"
        )
        result = await use_case.execute(project_id=1, method="GET", user=user)

        assert result.status_code == 500
        assert result.body == {
            "message": "Error Repository Server",
            "type": "Error Server",
        }

    async def test_get_project_use_case_success(self):
        except_return = {**data, "id": 1, "images_urls": ["image_url"]}
        del except_return["images_uploads"]
        repository.get_by_id_dict.side_effect = lambda *args, **kwargs: except_return
        result = await use_case.execute(project_id=1, method="GET", user=user)

        assert result.status_code == 200
        assert result.body == except_return
