import pytest
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.use_case.implements.post.tests.setup import repository, use_case, user, data


@pytest.mark.asyncio
class TestDeletePostUseCase:

    async def test_delete_post_post_id_not_found(self):
        repository.get_by_id_dict.side_effect = lambda *args, **kwargs: None
        result = await use_case.execute(user=user, post_id=data["id"], method="DELETE")

        assert result.status_code == 404
        assert result.body == {"message": "Post not found"}

    async def test_delete_post_use_case_Exception(self):
        repository.get_by_id_dict.side_effect = lambda *args, **kwargs: {"user_id": 1}
        repository.delete.side_effect = ExceptionCustomPresentation(
            status_code=500, type="Error Server", message="Error Repository Server"
        )
        result = await use_case.execute(user=user, post_id=data["id"], method="DELETE")

        assert result.status_code == 500
        assert result.body == {
            "message": "Error Repository Server",
            "type": "Error Server",
        }

    async def test_delete_post_use_case_success(self):
        repository.delete.side_effect = lambda *args, **kwargs: {
            "id": 1,
            "html": data["html"],
            "user_id": 1,
        }
        result = await use_case.execute(user=user, post_id=data["id"], method="DELETE")

        assert result.status_code == 204
        assert result.body == {}
