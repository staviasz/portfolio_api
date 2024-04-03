import copy
import pytest
from src.domain.models.project_models_domain import ProjectModelUpdateDomain
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.use_case.implements.project.test.setup import (
    use_case,
    bucket,
    data,
    repository,
    user,
)

new_data = ProjectModelUpdateDomain(**data)


@pytest.mark.asyncio
class TestEditProjectUseCase:
    async def test_upload_exception(self):
        bucket.upload.side_effect = ExceptionCustomPresentation(
            status_code=500, type="Error Server", message="Error Upload Server"
        )
        response = await use_case.execute(data=new_data, user=user, project_id=1)

        assert response.status_code == 500
        assert response.body == {
            "message": "Error Upload Server",
            "type": "Error Server",
        }

    async def test_success(self):
        repository_return = {**data, "images_urls": ["image_url"]}
        del repository_return["images_uploads"]
        repository_return["id"] = 1
        bucket.upload.side_effect = lambda *args, **kwargs: "image_url"
        repository.update_with_related.side_effect = (
            lambda *args, **kwargs: repository_return
        )
        response = await use_case.execute(data=new_data, user=user, project_id=1)

        assert response.status_code == 200
        assert response.body == repository_return

    async def test_update_with_related_exception(self):
        repository.update_with_related.side_effect = ExceptionCustomPresentation(
            status_code=500, type="Error Server", message="Error Repository Server"
        )
        response = await use_case.execute(data=new_data, user=user, project_id=1)

        assert response.status_code == 500
        assert response.body == {
            "message": "Error Repository Server",
            "type": "Error Server",
        }

    async def test_without_images(self):
        _data = copy.deepcopy(new_data)
        _data.images_uploads = None
        repository_return = {**_data.model_dump(), "images_urls": ["image_url"]}
        del repository_return["images_uploads"]
        repository_return["id"] = 1

        repository.update.side_effect = lambda *args, **kwargs: repository_return
        response = await use_case.execute(data=_data, user=user, project_id=1)

        assert response.status_code == 200
        assert response.body == repository_return
