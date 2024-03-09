from typing_extensions import Protocol

from src.domain.models.user_models_domain import UserModelDomain


class JwtDecodeProtocolUseCase(Protocol):

    async def decode_jwt(self, token) -> UserModelDomain: ...
