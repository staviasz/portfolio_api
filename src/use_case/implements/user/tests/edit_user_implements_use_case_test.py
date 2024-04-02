import copy
import pytest
from src.domain.models.user_models_domain import UserModelUpdateDomain

from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.use_case.implements.user.tests.setup import (
    use_case,
    data_user,
    repository,
    bucket,
)

data_update_user = UserModelUpdateDomain(**data_user)


user = {"id": 1, "image_url": "image_url", **data_user}
del user["image_upload"]


@pytest.mark.asyncio
class TestEditUserImplementsUseCase:
    async def test_get_by_email_exception(self):
        repository.get_by_email.side_effect = ExceptionCustomPresentation(
            status_code=500, type="Error Server", message="Error Email Server"
        )
        response = await use_case.execute(data_user=data_update_user, user=user)

        assert response.status_code == 500
        assert response.body == {
            "message": "Error Email Server",
            "type": "Error Server",
        }

    async def test_get_by_email_exists(self):
        repository.get_by_email.side_effect = lambda *args, **kwargs: {"id": 2}
        response = await use_case.execute(data_user=data_update_user, user=user)

        assert response.status_code == 409
        assert response.body["message"] == "Email already exists"

    async def test_get_by_email_success(self):
        user["email"] = "email@teste.com"
        update_user = user.copy()

        repository.get_by_email.side_effect = lambda *args, **kwargs: {"id": 1}
        repository.update.side_effect = lambda *args, **kwargs: update_user
        response = await use_case.execute(data_user=data_update_user, user=user)

        del update_user["password"]
        assert response.status_code == 200
        assert response.body == update_user

    async def test_upload_exception(self):
        bucket.update_upload.side_effect = ExceptionCustomPresentation(
            status_code=500, type="Error Server", message="Error Upload Server"
        )
        response = await use_case.execute(data_user=data_update_user, user=user)

        assert response.status_code == 500
        assert response.body == {
            "message": "Error Upload Server",
            "type": "Error Server",
        }

    async def test_upload_success(self):
        update_user = user.copy()
        update_user["name"] = "teste_update"
        bucket.update_upload.side_effect = lambda *args, **kwargs: "image_url"
        repository.update.side_effect = lambda *args, **kwargs: update_user
        response = await use_case.execute(data_user=data_update_user, user=user)

        del update_user["password"]
        assert response.status_code == 200
        assert response.body == update_user

    async def test_update_with_techs(self):
        new_data = copy.deepcopy(data_update_user)
        new_data.techs = [1, 2]
        new_user = {**user, "techs": ["react", "typescript"]}

        repository.get_by_id_dict.side_effect = lambda *args, **kwargs: [1, 2]
        repository.update_with_related.side_effect = lambda *args, **kwargs: new_user
        response = await use_case.execute(data_user=new_data, user=user)

        del new_user["password"]
        assert response.status_code == 200
        assert response.body == new_user

    async def test_update_with_techs_get_by_id_dict_exception(self):
        new_data = copy.deepcopy(data_update_user)
        new_data.techs = [1, 2]

        repository.get_by_id_dict.side_effect = ExceptionCustomPresentation(
            type="Error Server", status_code=500, message="Error Repository Server"
        )
        response = await use_case.execute(data_user=new_data, user=user)

        assert response.status_code == 500
        assert response.body == {
            "message": "Error Repository Server",
            "type": "Error Server",
        }

    async def test_update_exception(self):
        repository.update.side_effect = ExceptionCustomPresentation(
            status_code=500, type="Error Server", message="Error Repository Server"
        )
        response = await use_case.execute(data_user=data_update_user, user=user)

        assert response.status_code == 500
        assert response.body == {
            "message": "Error Repository Server",
            "type": "Error Server",
        }
