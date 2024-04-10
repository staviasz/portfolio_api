import pytest
from src.domain.models.post_models_domain import PostCreateModelDomain
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.use_case.implements.post.tests.setup import repository, use_case, data, user


new_data = PostCreateModelDomain(**data, techs=[1, 2, 3])


@pytest.mark.asyncio
class TestPostUseCase:
    async def test_create_post_use_case_exception(self):
        repository.create_with_related.side_effect = ExceptionCustomPresentation(
            status_code=500, type="Error Server", message="Error Repository Server"
        )
        response = await use_case.execute(data=new_data, user=user)

        assert response.status_code == 500
        assert response.body == {
            "message": "Error Repository Server",
            "type": "Error Server",
        }

    async def test_create_post_use_case(self):
        repository.create_with_related.side_effect = lambda *args, **kwargs: {
            "id": 1,
            "html": new_data.html,
            "name": new_data.name,
            "user_id": user.id,
            "images_urls": [str(url) for url in new_data.images_urls],
        }
        response = await use_case.execute(data=new_data, user=user)

        assert response.status_code == 201
        assert response.body == {
            "id": 1,
            "html": new_data.html,
            "name": new_data.name,
            "user_id": user.id,
            "images_urls": [str(url) for url in new_data.images_urls],
        }

    async def test_create_post_use_case_with_techs_exception_in_get_by_id(self):
        repository.get_by_id_dict.side_effect = ExceptionCustomPresentation(
            status_code=500, type="Error Server", message="Error Repository Server"
        )
        response = await use_case.execute(data=new_data, user=user)

        assert response.status_code == 500
        assert response.body == {
            "message": "Error Repository Server",
            "type": "Error Server",
        }

    async def test_create_post_use_case_with_techs_success(self):
        repository.get_by_id_dict.side_effect = lambda *args, **kwargs: [
            {"id": 1},
            {"id": 2},
        ]
        repository.create_with_related.side_effect = lambda *args, **kwargs: {
            "id": 1,
            "html": new_data.html,
            "name": new_data.name,
            "user_id": user.id,
            "images_urls": [str(url) for url in new_data.images_urls],
            "techs": ["react", "python"],
        }
        response = await use_case.execute(data=new_data, user=user)

        assert response.status_code == 201
        assert response.body == {
            "id": 1,
            "name": "name Post",
            "html": "<>post html</>",
            "images_urls": ["http://url1/", "http://url2/"],
            "user_id": 1,
            "techs": ["react", "python"],
        }
