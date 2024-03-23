from src.domain.protocols.use_case_protocol_domain import DomainProtocol
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.presentation.types.http_types_presentation import HttpResponse
from src.presentation.types.image_upload_type_presentation import ImageUpload
from src.use_case.protocols.aws.aws_protocol_use_case import AwsProtocolUseCase


class UploadImageUseCase(DomainProtocol):
    def __init__(self, bucket: AwsProtocolUseCase) -> None:
        self.bucket = bucket

    async def execute(
        self, images_uploads: ImageUpload | list[ImageUpload], folder_name: str
    ) -> HttpResponse:
        try:
            response = await self.bucket.upload(folder=folder_name, file=images_uploads)
            return HttpResponse(
                status_code=200,
                body=response if isinstance(response, list) else [response],
            )
        except ExceptionCustomPresentation as error:
            return HttpResponse(status_code=error.status_code, body=error.body)
