from src.presentation.contracts.middleware_contract_presentation import (
    MiddlewareContract,
)
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)

from src.presentation.types.http_types_presentation import HttpRequest
from src.use_case.protocols.jwt.decode_jwt_protocol_use_case import (
    JwtDecodeProtocolUseCase,
)


class AuthMiddleware(MiddlewareContract):

    def __init__(self, autenticator: JwtDecodeProtocolUseCase):
        self.autenticator = autenticator

    async def execute(self, request: HttpRequest) -> dict | None:
        try:
            token = request.headers.get("Authorization") if request.headers else None

            if not token:
                raise ExceptionCustomPresentation(
                    status_code=401, type="unauthorized", message="No token provided"
                )

            payload = await self.autenticator.decode(token)

            return payload.model_all_dump()

        except Exception:
            raise ExceptionCustomPresentation(
                status_code=401, type="unauthorized", message="Invalid token"
            )
