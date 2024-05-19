import jsonwebtoken
from src.configs.pydantic.pydantic_env_settings_config import PydanticEnv
from src.domain.models.user_models_domain import UserModelDomain
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.use_case.protocols.jwt.jwt_protocol_use_case import JwtProtocolUseCase


class AuthJwtInfra(JwtProtocolUseCase):
    async def encode(self, payload: UserModelDomain) -> str:
        try:
            payload_dict = payload.model_all_dump()
            token = jsonwebtoken.encode(
                payload_dict, PydanticEnv().jwt_secret_key, algorithm="HS256"
            )
            return token
        except Exception as error:
            raise ExceptionCustomPresentation(
                status_code=500,
                type="Server Error",
                message="Auth encode error",
                error=error.args,
            )

    async def decode(self, token: str) -> UserModelDomain:
        try:
            payload = jsonwebtoken.decode(
                token, PydanticEnv().jwt_secret_key, algorithms=["HS256"]
            )
            user = UserModelDomain(**payload)
            return user

        except Exception as error:
            raise ExceptionCustomPresentation(
                status_code=500,
                type="Server Error",
                message="Auth decode error",
                error=error.args,
            )
