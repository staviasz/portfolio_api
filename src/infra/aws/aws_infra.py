from datetime import datetime
import re
from src.configs.pydantic.pydantic_env_settings_config import PydanticEnv
from src.domain.models.user_models_domain import ImageUpload
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.use_case.protocols.aws.aws_protocol_use_case import AwsProtocolUseCase


class AwsInfra(AwsProtocolUseCase):

    def __init__(self, client):
        self.client = client

    async def upload(
        self, folder: str, file: ImageUpload | list[ImageUpload]
    ) -> str | list[str]:
        try:
            if isinstance(file, ImageUpload):
                new_filename = self.slug(file.filename)
                self.client.put_object(
                    Bucket=PydanticEnv().bucket_name,
                    Key=f"{folder}/{new_filename}",
                    Body=file.body,
                    ContentType=file.mimetype,
                )
                return self.create_url(folder, new_filename)

            if isinstance(file, list):
                uploads = []
                for f in file:
                    new_filename = self.slug(f.filename)
                    self.client.put_object(
                        Bucket=PydanticEnv().bucket_name,
                        Key=f"{folder}/{new_filename}",
                        Body=f.body,
                        ContentType=f.mimetype,
                    )
                    uploads.append(self.create_url(folder, new_filename))

                return uploads

        except Exception as error:
            raise ExceptionCustomPresentation(
                status_code=500,
                message="Error on upload",
                type="Server Error",
                error=error,
            )

    async def update_upload(
        self,
        last_url_file: str | list[str],
        folder: str,
        file: ImageUpload | list[ImageUpload],
    ) -> str | list[str]:
        try:
            await self.delete_upload(last_url_file)

            return await self.upload(folder, file)

        except Exception as error:
            raise ExceptionCustomPresentation(
                status_code=500,
                message="Error on update_upload",
                type="Server Error",
                error=error,
            )

    async def delete_upload(self, last_url_file: str | list[str]) -> None:
        try:
            if isinstance(last_url_file, list):
                for url_file in last_url_file:
                    self.client.delete_object(
                        Bucket=PydanticEnv().bucket_name, Key=url_file.split(".com/")[1]
                    )
                return

            self.client.delete_object(
                Bucket=PydanticEnv().bucket_name, Key=last_url_file.split(".com/")[1]
            )
            return

        except Exception as error:
            raise ExceptionCustomPresentation(
                status_code=500,
                message="Error on delete_upload",
                type="Server Error",
                error=error,
            )

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
