from datetime import datetime
import re
from src.configs.pydantic.pydantic_env_settings_config import PydanticEnv
from src.domain.models.user_models_domain import ImageUpload
from src.use_case.protocols.aws.aws_protocol_use_case import AwsProtocolUseCase


class AwsInfra(AwsProtocolUseCase):

    def __init__(self, client):
        self.client = client

    async def upload(self, folder: str, file: ImageUpload) -> str:

        new_filename = self.slug(file.filename)
        self.client.put_object(
            Bucket=PydanticEnv().bucket_name,
            Key=f"{folder}/{new_filename}",
            Body=file.body,
            ContentType=file.mimetype,
        )
        return self.create_url(folder, new_filename)

    async def update_upload(
        self, last_url_file: str, folder: str, file: ImageUpload
    ) -> str:
        await self.delete_upload(last_url_file)
        return await self.upload(folder, file)

    async def delete_upload(self, last_url_file: str) -> None:
        self.client.delete_object(Bucket=PydanticEnv().bucket_name, Key=last_url_file)
        return

    def slug(self, file_name: str) -> str:
        text_split = file_name.split(".")
        ext = text_split.pop()
        date = datetime.now()
        format_regex = re.sub(
            r"\d",
            "",
            re.sub(
                r"\s+",
                "-",
                re.sub(
                    r"-+",
                    "-",
                    re.sub(r"[^\w\s]", "", " ".join(text_split).lower().strip()),
                ),
            ),
        )

        return f"{format_regex}{int(date.timestamp())}.{ext}"

    def create_url(self, folder: str, file_name: str) -> str:
        return f"https://{PydanticEnv().bucket_name}.{PydanticEnv().bucket_endpoint}/{folder}/{file_name}"
