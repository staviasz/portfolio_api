import copy
import io
import os
from unittest.mock import Mock

from fastapi import UploadFile
from fastapi.datastructures import Headers
import pytest
from src.domain.protocols.project_protocols_domain import ProjectDomainProtocol
from src.infra.pydantic.validator_schema_infra import ValidatorSchemaInfra
from src.presentation.controllers.projects.projects_controller_presentation import (
    ProjectsControllerPresentation,
)
from src.presentation.types.http_types_presentation import HttpRequest, HttpResponse
from src.presentation.validators.schemas.project_create_schema_presentation import (
    ProjectCreateSchema,
)


validator = ValidatorSchemaInfra()
schema = ProjectCreateSchema
use_case = Mock(spec_set=ProjectDomainProtocol)

controller = ProjectsControllerPresentation(
    validator=validator, schema=schema, use_case=use_case
)


request: HttpRequest = HttpRequest(
    params={"id": 1},
    headers={
        "method": "POST",
    },
    body={
        "name": "name teste",
        "description": "description" * 10,
        "link_deploy": "https://github.com",
        "link_code": "https://github.com",
    },
)

kwargs = {
    "args": {
        "id": 1,
        "name": "name",
        "email": "email@teste.com",
        "password": "@Teste123",
        "description": "<>description" * 10,
        "contact_description": "contact_description" * 10,
    },
}

current_dir = os.path.dirname(__file__)
test_file = os.path.abspath(os.path.join(current_dir, "../../../../test.txt"))

file = None
with open(test_file, "rb") as f:
    file_body = f.read()
    file_object = io.BytesIO(file_body)
    file = [
        UploadFile(
            filename="test.txt",
            headers=Headers(headers={"Content-Type": "text/plain"}),
            file=file_object,
        )
    ]


@pytest.mark.asyncio
class TestProjectControllerPresentation:

    async def test_execute_with_files_form_data_no_request_and_no_files(self):
        response = await controller.execute_with_files_form_data(
            request=None, files=None
        )

        assert response.status_code == 400
        assert response.body == {"message": "Request or files must be provided"}

    async def test_execute_with_files_form_data_name_required(self):
        new_request = copy.deepcopy(request)
        del new_request.body["name"]
        response = await controller.execute_with_files_form_data(new_request, file)

        body = response.body
        except_error = {"field": "name", "type": "missing", "message": "Field required"}

        assert response.status_code == 422
        assert isinstance(body, list)
        assert body[0] == except_error

    async def test_execute_with_files_form_data_name_have_min_3_letters(self):
        new_request = copy.deepcopy(request)
        new_request.body["name"] = "te"
        response = await controller.execute_with_files_form_data(new_request, file)

        body = response.body
        except_error = {
            "field": "name",
            "type": "string_too_short",
            "message": "String should have at least 5 characters",
        }

        assert response.status_code == 422
        assert isinstance(body, list)
        assert body[0] == except_error

    async def test_execute_with_files_form_data_name_have_max_150_letters(self):
        new_request = copy.deepcopy(request)
        new_request.body["name"] = "teste" * 50
        response = await controller.execute_with_files_form_data(new_request, file)

        body = response.body
        except_error = {
            "field": "name",
            "type": "string_too_long",
            "message": "String should have at most 150 characters",
        }

        assert response.status_code == 422
        assert isinstance(body, list)
        assert body[0] == except_error

    async def test_execute_with_files_form_data_description_is_min_50(self):
        new_request = copy.deepcopy(request)
        new_request.body["description"] = "test"
        response = await controller.execute_with_files_form_data(new_request, file)

        body = response.body
        except_error = {
            "field": "description",
            "type": "string_too_short",
            "message": "String should have at least 50 characters",
        }

        assert response.status_code == 422
        assert isinstance(body, list)
        assert body[0] == except_error

    async def test_execute_with_files_form_data_link_is_url(self):
        new_request = copy.deepcopy(request)
        new_request.body["link_deploy"] = "teste"
        response = await controller.execute_with_files_form_data(new_request, file)

        body = response.body
        except_error = {
            "field": "link_deploy",
            "type": "url_parsing",
            "message": "Input should be a valid URL, relative URL without a base",
        }

        assert response.status_code == 422
        assert isinstance(body, list)
        assert body[0] == except_error

    async def test_execute_with_files_form_data_exception(self):
        use_case.execute.side_effect = Exception("Error Server")
        response = await controller.execute_with_files_form_data(request, file)

        assert response.status_code == 500
        assert isinstance(response.body["Error"], Exception)
        assert str(response.body["Error"]) == "Error Server"

    async def test_execute_with_files_form_data_success(self):
        use_case.execute.side_effect = lambda *args, **kwargs: HttpResponse(
            status_code=200, body={"message": "Success"}
        )
        response = await controller.execute_with_files_form_data(request, file)

        assert response.status_code == 200
        assert response.body == {"message": "Success"}

    async def test_execute_json_exception(self):
        use_case.execute.side_effect = Exception("Error Server")
        response = await controller.execute_json(request)

        assert response.status_code == 500
        assert isinstance(response.body["Error"], Exception)
        assert str(response.body["Error"]) == "Error Server"

    async def test_execute_json_success(self):
        use_case.execute.side_effect = lambda *args, **kwargs: HttpResponse(
            status_code=200, body={"message": "Success"}
        )
        response = await controller.execute_json(request)

        assert response.status_code == 200
        assert response.body == {"message": "Success"}
