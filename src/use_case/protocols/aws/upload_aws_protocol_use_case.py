from typing_extensions import Protocol

from src.domain.models.user_models_domain import ImageUpload


class AwsUploadProtocolUseCase(Protocol):

    async def upload(self, folder: str, file: ImageUpload) -> str: ...

    async def update_upload(
        self, last_url_file: str, folder: str, file: ImageUpload
    ) -> str: ...

    async def delete_upload(self, last_url_file: str) -> None: ...
