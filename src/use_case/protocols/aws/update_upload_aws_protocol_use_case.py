from typing_extensions import Protocol

from src.domain.models.user_models_domain import ImageUpload


class AwsUpdateUploadProtocolUseCase(Protocol):

    async def update_upload(
        self,
        last_url_file: str | list[str],
        folder: str,
        file: ImageUpload | list[ImageUpload],
    ) -> str | list[str]: ...
