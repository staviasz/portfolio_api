import boto3
from botocore.config import Config
from src.configs.pydantic.pydantic_env_settings_config import PydanticEnv


s3_client = boto3.client(
    service_name="s3",
    endpoint_url=f"http://{PydanticEnv().bucket_endpoint}",
    aws_secret_access_key=PydanticEnv().bucket_app_key,
    aws_access_key_id=PydanticEnv().bucket_key_id,
    config=Config(signature_version="s3v4"),
)
