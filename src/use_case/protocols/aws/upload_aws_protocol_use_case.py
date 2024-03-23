from typing_extensions import Protocol

from src.domain.models.user_models_domain import ImageUpload


class AwsUploadProtocolUseCase(Protocol):

    async def upload(
        self, folder: str, file: ImageUpload | list[ImageUpload]
    ) -> str | list[str]: ...
