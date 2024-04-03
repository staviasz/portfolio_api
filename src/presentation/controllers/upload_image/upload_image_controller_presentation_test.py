import io
import os
from unittest.mock import Mock

from fastapi import UploadFile
from fastapi.datastructures import Headers
import pytest
from src.domain.protocols.use_case_protocol_domain import DomainProtocol
from src.infra.pydantic.validator_schema_infra import ValidatorSchemaInfra
from src.presentation.controllers.upload_image.upload_image_controller_presentation import (
    UploadImageController,
)
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.presentation.types.http_types_presentation import HttpRequest, HttpResponse
from src.presentation.validators.schemas.upload_image_schema_presentation import (
    UploadImageSchema,
)

validator = ValidatorSchemaInfra()
schema = UploadImageSchema
use_case = Mock(spec_set=DomainProtocol)
controller = UploadImageController(
    use_case=use_case, validator=validator, schema=schema
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
class TestUploadImageController:
    async def test_upload_image_without_body(self):
        response = await controller.execute_with_files_form_data(
            request=HttpRequest(body=None), files=file
        )
        assert response.status_code == 400
        assert response.body == {"message": "File or body not found"}

    async def test_upload_image_without_file(self):
        data = HttpRequest(body={"folder_name": "folder_name"})
        response = await controller.execute_with_files_form_data(
            request=data, files=None
        )
        assert response.status_code == 400
        assert response.body == {"message": "File or body not found"}

    async def test_upload_image_folder_name_is_required(self):
        data = HttpRequest(body={"test": "test"})
        response = await controller.execute_with_files_form_data(
            request=data, files=file
        )

        assert response.status_code == 422
        assert response.body == [
            {"field": "folder_name", "type": "missing", "message": "Field required"}
        ]

    async def test_upload_image_folder_name_is_string(self):
        data = HttpRequest(body={"folder_name": 1})
        response = await controller.execute_with_files_form_data(
            request=data, files=file
        )

        assert response.status_code == 422
        assert response.body == [
            {
                "field": "folder_name",
                "type": "string_type",
                "message": "Input should be a valid string",
            }
        ]

    async def test_upload_image_folder_name_min_length(self):
        data = HttpRequest(body={"folder_name": "a"})
        response = await controller.execute_with_files_form_data(
            request=data, files=file
        )

        assert response.status_code == 422
        assert response.body == [
            {
                "field": "folder_name",
                "type": "string_too_short",
                "message": "String should have at least 5 characters",
            }
        ]

    async def test_upload_image_folder_name_max_length(self):
        data = HttpRequest(body={"folder_name": "a" * 21})
        response = await controller.execute_with_files_form_data(
            request=data, files=file
        )

        assert response.status_code == 422
        assert response.body == [
            {
                "field": "folder_name",
                "type": "string_too_long",
                "message": "String should have at most 20 characters",
            }
        ]

    async def test_upload_image_exception(self):
        use_case.execute.side_effect = ExceptionCustomPresentation(
            status_code=500, type="Error Server", message="Error UseCase Server"
        )
        data = HttpRequest(body={"folder_name": "folder_name"})
        response = await controller.execute_with_files_form_data(
            request=data, files=file
        )

        assert response.status_code == 500
        assert response.body == {
            "message": "Error UseCase Server",
            "type": "Error Server",
        }

    async def test_upload_image_success(self):
        use_case.execute.side_effect = lambda *args, **kwargs: HttpResponse(
            status_code=200, body=["image_url"]
        )
        data = HttpRequest(body={"folder_name": "folder_name"})
        response = await controller.execute_with_files_form_data(
            request=data, files=file
        )

        assert response.status_code == 200
        assert response.body == ["image_url"]
