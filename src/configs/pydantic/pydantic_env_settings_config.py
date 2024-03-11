from pydantic import Field
from pydantic_settings import BaseSettings
import dotenv

dotenv.load_dotenv()


class PydanticEnv(BaseSettings):
    env: str = Field(..., env="ENV")
    port: int = Field(..., env="PORT")
    bucket_name: str = Field(..., env="BUCKET_NAME")
    bucket_key_id: str = Field(..., env="BUCKET_KEY_ID")
    bucket_endpoint: str = Field(..., env="BUCKET_ENDPOINT")
    bucket_app_key: str = Field(..., env="BUCKET_APP_KEY")
    database_url: str = Field(..., env="DATABASE_URL")
    jwt_secret_key: str = Field(..., env="JWT_SECRET_KEY")
