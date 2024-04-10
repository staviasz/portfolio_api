from typing_extensions import Protocol


class AwsDeleteProtocolUseCase(Protocol):

    async def delete_upload(self, last_url_file: list[str] | str) -> None: ...
