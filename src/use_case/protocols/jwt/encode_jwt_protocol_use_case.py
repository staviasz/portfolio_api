from typing_extensions import Protocol

from src.domain.models.user_models_domain import UserModelDomain


class JwtEncodeProtocolUseCase(Protocol):
    async def encode(self, payload: UserModelDomain) -> str: ...
