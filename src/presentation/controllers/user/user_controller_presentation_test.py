import copy
import io
import os
from unittest.mock import Mock

from fastapi import UploadFile
from fastapi.datastructures import Headers
import pytest
from src.domain.protocols.user_protocols_domain import UserDomainProtocol
from src.infra.pydantic.validator_schema_infra import ValidatorSchemaInfra
from src.presentation.controllers.user.user_controller_presentation import (
    UserControllerPresentation,
)
from src.presentation.types.http_types_presentation import HttpRequest, HttpResponse
from src.presentation.validators.schemas.user_create_schema_presentation import (
    UserCreateSchema,
)

validator = ValidatorSchemaInfra()
schema = UserCreateSchema
use_case = Mock(spec_set=UserDomainProtocol)

controller = UserControllerPresentation(
    validator=validator, schema=schema, use_case=use_case
)

request: HttpRequest = HttpRequest(
    headers={
        "method": "POST",
        "user": "user",
    },
    body={
        "name": "name",
        "email": "email@teste.com",
        "password": "@Teste123",
        "description": "<>description" * 10,
        "contact_description": "contact_description" * 10,
    },
)

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
class TestUserControllerPresentation:

    async def test_execute_with_files_form_data_no_request(self):
        new_request = copy.deepcopy(request)
        new_request.headers = None
        response = await controller.execute_with_files_form_data(new_request, file)

        assert response.status_code == 400
        assert response.body == {"message": "Request not found"}

        new_request.headers = request.headers
        new_request.body = None
        response = await controller.execute_with_files_form_data(new_request, file)

        assert response.status_code == 400
        assert response.body == {"message": "Request not found"}

    async def test_execute_with_files_form_data_name_required(self):
        new_request = copy.deepcopy(request)
        del new_request.body["name"]
        response = await controller.execute_with_files_form_data(new_request, file)

        body = response.body
        except_error = {"field": "name", "type": "missing", "message": "Field required"}

        assert response.status_code == 422
        assert isinstance(body, list)
        assert body[0] == except_error

    async def test_execute_with_files_form_data_name_is_only_letters(self):
        new_request = copy.deepcopy(request)
        new_request.body["name"] = "teste123"
        response = await controller.execute_with_files_form_data(new_request, file)

        body = response.body
        except_error = {
            "field": "name",
            "type": "value_error",
            "message": "Value error, Name must be only letters",
        }

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
            "message": "String should have at least 3 characters",
        }

        assert response.status_code == 422
        assert isinstance(body, list)
        assert body[0] == except_error

    async def test_execute_with_files_form_data_email_is_valid(self):
        new_request = copy.deepcopy(request)
        new_request.body["email"] = "invalidEmail"
        response = await controller.execute_with_files_form_data(new_request, file)

        body = response.body
        except_error = {
            "field": "email",
            "type": "value_error",
            "message": """value is not a valid email address: The email address is not valid. It must have exactly one @-sign.""",
        }

        assert response.status_code == 422
        assert isinstance(body, list)
        assert body[0] == except_error

    async def test_execute_with_files_form_data_password_is_valid(self):
        new_request = copy.deepcopy(request)
        new_request.body["password"] = "invalidPassword"
        response = await controller.execute_with_files_form_data(new_request, file)

        body = response.body
        except_error = {
            "field": "  Value error, Password must contain at least one lowercase letter, one uppercase letter,",
            "type": "value_error",
            "message": "one digit, one special character, and be at least 8 characters long",
        }

        assert response.status_code == 422
        assert isinstance(body, list)
        assert body[0] == except_error

    async def test_execute_with_files_form_data_description_is_html(self):
        new_request = copy.deepcopy(request)
        new_request.body["description"] = "test" * 20
        response = await controller.execute_with_files_form_data(new_request, file)

        body = response.body
        except_error = {
            "field": "description",
            "type": "value_error",
            "message": "Value error, Description must be html",
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

    async def test_execute_with_files_form_data_contact_description_is_min_50(self):
        new_request = copy.deepcopy(request)
        new_request.body["contact_description"] = "test"
        response = await controller.execute_with_files_form_data(new_request, file)

        body = response.body
        except_error = {
            "field": "contact_description",
            "type": "string_too_short",
            "message": "String should have at least 50 characters",
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

    async def test_execute_json_no_request(self):
        new_request = copy.deepcopy(request)
        new_request.headers = None
        response = await controller.execute_json(new_request)

        assert response.status_code == 400
        assert response.body == {"message": "Request not found"}

        new_request.headers = request.headers
        new_request.body = None
        response = await controller.execute_json(new_request)

        assert response.status_code == 400
        assert response.body == {"message": "Request not found"}

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
