import pytest
from src.domain.models.post_models_domain import PostUpdatesModelDomain
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.use_case.implements.post.tests.setup import repository, use_case, data, user

new_data = PostUpdatesModelDomain(**data)


@pytest.mark.asyncio
class TestUpdatePostUseCase:

    async def test_update_post_post_id_not_found(self):
        repository.get_by_id_dict.side_effect = lambda *args, **kwargs: None
        result = await use_case.execute(data=new_data, user=user, post_id=1)

        assert result.status_code == 404
        assert result.body == {"message": "Post not found"}

    async def test_update_post_use_case_Exception(self):
        repository.get_by_id_dict.side_effect = lambda *args, **kwargs: {"user_id": 1}
        repository.update.side_effect = ExceptionCustomPresentation(
            status_code=500, type="Error Server", message="Error Repository Server"
        )
        result = await use_case.execute(data=new_data, user=user, post_id=1)

        assert result.status_code == 500
        assert result.body == {
            "message": "Error Repository Server",
            "type": "Error Server",
        }

    async def test_update_post_use_case_success(self):
        repository.update.side_effect = lambda *args, **kwargs: {
            "id": 1,
            "name": new_data.name,
            "html": new_data.html,
            "user_id": 1,
            "images_urls": [str(url) for url in new_data.images_urls],
        }
        result = await use_case.execute(data=new_data, user=user, post_id=1)

        assert result.status_code == 200
        assert result.body == {
            "id": 1,
            "name": new_data.name,
            "html": new_data.html,
            "user_id": 1,
            "images_urls": [str(url) for url in new_data.images_urls],
        }
