import pytest
from src.domain.models.project_models_domain import ProjectModelCreateDomain
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.use_case.implements.project.test.setup import (
    bucket,
    use_case,
    data,
    user,
    repository,
)

new_data = ProjectModelCreateDomain(**data)


@pytest.mark.asyncio
class TestAddProjectUseCase:
    async def test_upload_exception(self):
        bucket.upload.side_effect = ExceptionCustomPresentation(
            status_code=500, type="Error Server", message="Error Upload Server"
        )
        response = await use_case.execute(data=new_data, user=user)

        assert response.status_code == 500
        assert response.body == {
            "message": "Error Upload Server",
            "type": "Error Server",
        }

    async def test_success(self):
        repository_return = {**new_data.model_dump(), "images_urls": ["image_url"]}
        del repository_return["images_uploads"]
        repository_return["id"] = 1

        bucket.upload.side_effect = lambda *args, **kwargs: "image_url"
        repository.create_with_related.side_effect = (
            lambda *args, **kwargs: repository_return
        )
        response = await use_case.execute(data=new_data, user=user)

        assert response.status_code == 201
        assert response.body == repository_return

    async def test_repository_exception(self):
        repository.create_with_related.side_effect = ExceptionCustomPresentation(
            status_code=500, type="Error Server", message="Error Repository Server"
        )
        response = await use_case.execute(data=new_data, user=user)

        assert response.status_code == 500
        assert response.body == {
            "message": "Error Repository Server",
            "type": "Error Server",
        }
