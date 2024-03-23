import copy
from unittest.mock import Mock

import pytest
from src.domain.protocols.use_case_protocol_domain import DomainProtocol
from src.infra.pydantic.validator_schema_infra import ValidatorSchemaInfra
from src.presentation.controllers.login.login_controller_presentation import (
    LoginControllerPresentation,
)
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.presentation.types.http_types_presentation import HttpRequest, HttpResponse
from src.presentation.validators.schemas.login_schema_presentation import (
    LoginSchemaPresentation,
)


validator = ValidatorSchemaInfra()
schema = LoginSchemaPresentation
use_case = Mock(spec_set=DomainProtocol)

controller = LoginControllerPresentation(
    validator=validator, schema=schema, use_case=use_case
)

request = HttpRequest(body={"email": "email@email.com", "password": "@Teste123"})


@pytest.mark.asyncio
class TestLoginControllerPresentation:
    async def test_missing_body(self):
        new_request = HttpRequest(body=None)
        response = await controller.execute_json(new_request)
        assert response.status_code == 400
        assert response.body == {"message": "Missing body"}

    async def test_email_is_required(self):
        new_request = copy.deepcopy(request)
        del new_request.body["email"]
        response = await controller.execute_json(new_request)

        expect_body = [
            {"field": "email", "type": "missing", "message": "Field required"}
        ]

        assert response.status_code == 422
        assert response.body == expect_body

    async def test_password_is_required(self):
        new_request = copy.deepcopy(request)
        del new_request.body["password"]
        response = await controller.execute_json(new_request)

        expect_body = [
            {"field": "password", "type": "missing", "message": "Field required"}
        ]

        assert response.status_code == 422
        assert response.body == expect_body

    async def test_password_is_min_8(self):
        new_request = copy.deepcopy(request)
        new_request.body["password"] = "teste"
        response = await controller.execute_json(new_request)

        expect_body = [
            {
                "field": "password",
                "type": "string_too_short",
                "message": "String should have at least 8 characters",
            }
        ]

        assert response.status_code == 422
        assert response.body == expect_body

    async def test_password_is_max_20(self):
        new_request = copy.deepcopy(request)
        new_request.body["password"] = "teste" * 10
        response = await controller.execute_json(new_request)

        expect_body = [
            {
                "field": "password",
                "type": "string_too_long",
                "message": "String should have at most 20 characters",
            }
        ]

        assert response.status_code == 422
        assert response.body == expect_body

    async def test_password_is_valid(self):
        new_request = copy.deepcopy(request)
        new_request.body["password"] = "testeteste"
        response = await controller.execute_json(new_request)

        expect_body = [
            {
                "field": "  Value error, Password must contain at least one lowercase letter, one uppercase letter,",
                "type": "value_error",
                "message": "one digit, one special character, and be at least 8 characters long",
            }
        ]

        assert response.status_code == 422
        assert response.body == expect_body

    async def test_use_case_exception(self):
        use_case.execute.side_effect = ExceptionCustomPresentation(
            status_code=500, message="Error UseCase Server", type="Error Server"
        )
        response = await controller.execute_json(request)

        assert response.status_code == 500
        assert response.body == {
            "message": "Error UseCase Server",
            "type": "Error Server",
        }

    async def test_use_case_success(self):
        use_case.execute.side_effect = lambda *args, **kwargs: HttpResponse(
            status_code=200, body={"token": "token"}
        )
        response = await controller.execute_json(request)

        assert response.status_code == 200
        assert response.body["token"] == "token"
