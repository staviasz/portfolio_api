import boto3
from botocore.config import Config
from src.configs.pydantic.pydantic_env_settings_config import PydanticEnv


class S3Client:

    def __init__(self, endpoint_url, aws_secret_access_key, aws_access_key_id):
        self.endpoint_url = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_access_key_id = aws_secret_access_key

    def create_client(self):
        return boto3.resource(
            service_name="s3",
            endpoint_url=self.endpoint_url,
            aws_secret_access_key=self.aws_secret_access_key,
            aws_access_key_id=self.aws_access_key_id,
            config=Config(signature_version="s3v4"),
        )


endpoint_url = f"http://{PydanticEnv().bucket_endpoint}"
aws_secret_access_key = PydanticEnv().bucket_app_key
aws_access_key_id = PydanticEnv().bucket_key_id

S3 = S3Client(
    endpoint_url=endpoint_url,
    aws_secret_access_key=aws_secret_access_key,
    aws_access_key_id=aws_access_key_id,
).create_client()
