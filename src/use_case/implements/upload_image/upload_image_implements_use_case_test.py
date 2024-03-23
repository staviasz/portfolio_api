from unittest.mock import Mock
import pytest

from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.use_case.implements.upload_image.upload_image_implements_use_case import (
    UploadImageUseCase,
)
from src.use_case.protocols.aws.aws_protocol_use_case import AwsProtocolUseCase


bucket = Mock(spec_set=AwsProtocolUseCase)
use_case = UploadImageUseCase(bucket=bucket)

images_uploads = {
    "filename": "teste.txt",
    "body": b"teste",
    "mimetype": "text/plain",
}


@pytest.mark.asyncio
class TestUploadImageUseCase:
    async def test_upload_image_use_case_exception(self):
        bucket.upload.side_effect = ExceptionCustomPresentation(
            status_code=500, type="Error Server", message="Error Upload Server"
        )

        response = await use_case.execute(images_uploads, folder_name="test")

        assert response.status_code == 500
        assert response.body == {
            "type": "Error Server",
            "message": "Error Upload Server",
        }

    async def test_upload_image_use_case_success(self):
        bucket.upload.side_effect = lambda *args, **kwargs: "teste.txt"

        response = await use_case.execute(images_uploads, folder_name="test")

        assert response.status_code == 200
        assert response.body == ["teste.txt"]
