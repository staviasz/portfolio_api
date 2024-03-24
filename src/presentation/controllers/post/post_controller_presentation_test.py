from unittest.mock import Mock
import pytest

from src.domain.protocols.post_protocols_domain import PostDomainProtocol
from src.infra.pydantic.validator_schema_infra import ValidatorSchemaInfra
from src.presentation.controllers.post.post_controller_presentation import (
    PostControllerPresentation,
)
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.presentation.types.http_types_presentation import HttpRequest, HttpResponse
from src.presentation.validators.schemas.post_schema_presentation import (
    PostSchemaPresentation,
)

validator = ValidatorSchemaInfra()
schema = PostSchemaPresentation
use_case = Mock(spec_set=PostDomainProtocol)
controller = PostControllerPresentation(
    validator=validator, schema=schema, use_case=use_case
)

body = {"html": "<>test de html</>" * 20}
params = {"post_id": 1}
method = {"method": "POST"}
query = {"filters": {"user_id": 1}}


@pytest.mark.asyncio
class TestPostController:
    async def test_execute_json_without_body(self):
        request = HttpRequest(params=params, headers=method, query=query)
        response = await controller.execute_json(request=request)

        assert response.status_code == 400
        assert response.body == {"message": "Request body must be provided"}

    async def test_execute_json_without_html_in_body(self):
        body = {"name": "test"}
        request = HttpRequest(body=body, params=params, headers=method, query=query)
        response = await controller.execute_json(request=request)

        assert response.status_code == 422
        assert response.body == [
            {
                "field": "html",
                "type": "missing",
                "message": "Field required",
            }
        ]

    async def test_execute_json_html_is_string(self):
        body = {"html": 1}
        request = HttpRequest(body=body, params=params, headers=method, query=query)
        response = await controller.execute_json(request=request)

        assert response.status_code == 422
        assert response.body == [
            {
                "field": "html",
                "type": "string_type",
                "message": "Input should be a valid string",
            }
        ]

    async def test_execute_json_html_is_min_50(self):
        body = {"html": "<>test de html</>"}
        request = HttpRequest(body=body, params=params, headers=method, query=query)
        response = await controller.execute_json(request=request)

        assert response.status_code == 422
        assert response.body == [
            {
                "field": "html",
                "type": "string_too_short",
                "message": "String should have at least 50 characters",
            }
        ]

    async def test_execute_json_exception(self):
        use_case.execute.side_effect = ExceptionCustomPresentation(
            status_code=500, type="Error Server", message="Error UseCase Server"
        )
        request = HttpRequest(body=body, params=params, headers=method, query=query)
        response = await controller.execute_json(request=request)

        assert response.status_code == 500
        assert response.body == {
            "type": "Error Server",
            "message": "Error UseCase Server",
        }

    async def test_execute_json_success(self):
        use_case.execute.side_effect = lambda *args, **kwargs: HttpResponse(
            status_code=200, body={"message": "Success"}
        )
        request = HttpRequest(body=body, params=params, headers=method, query=query)
        response = await controller.execute_json(request=request)

        assert response.status_code == 200
        assert response.body == {"message": "Success"}
