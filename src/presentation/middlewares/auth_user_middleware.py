from src.domain.models.user_models_domain import UserModelDomain
from src.infra.repository.models.user_model_repository_infra import User
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
from src.use_case.protocols.repository.repository_protocol_use_case import (
    RepositoryProtocolUseCase,
)


class AuthMiddleware(MiddlewareContract):

    def __init__(
        self,
        autenticator: JwtDecodeProtocolUseCase,
        repository: RepositoryProtocolUseCase,
    ):
        self.autenticator = autenticator
        self.repository = repository

    async def execute(self, request: HttpRequest) -> dict | None:
        try:
            token = request.headers.get("Authorization") if request.headers else None

            if not token:
                raise ExceptionCustomPresentation(
                    status_code=401, type="unauthorized", message="No token provided"
                )

            payload = await self.autenticator.decode(token)
            print(payload)

            user = await self.repository.get_by_id_dict(table_name=User, id=payload.id)

            if not user:
                raise ExceptionCustomPresentation(
                    status_code=401, type="unauthorized", message="User not found"
                )

            return UserModelDomain(**user).model_all_dump()

        except Exception as error:
            print(error)
            raise ExceptionCustomPresentation(
                status_code=401, type="unauthorized", message="Invalid token"
            )
