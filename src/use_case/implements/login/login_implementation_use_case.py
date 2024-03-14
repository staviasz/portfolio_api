from src.domain.models.login_models_domain import LoginModelDomain
from src.domain.models.user_models_domain import UserModelDomain
from src.domain.protocols.login_protocols_domain import LoginDomainProtocol
from src.infra.repository.models.user_model_repository_infra import User
from src.presentation.types.http_types_presentation import HttpResponse
from src.use_case.protocols.bycript.bycript_protocol_use_case import (
    BycryptProtocolUseCase,
)
from src.use_case.protocols.jwt.jwt_protocol_use_case import JwtProtocolUseCase
from src.use_case.protocols.repository.repository_protocol_use_case import (
    RepositoryProtocolUseCase,
)


class loginUseCase(LoginDomainProtocol):

    def __init__(
        self,
        repository: RepositoryProtocolUseCase,
        authenticator: JwtProtocolUseCase,
        hasher: BycryptProtocolUseCase,
    ) -> None:
        self.repository = repository
        self.authenticator = authenticator
        self.hasher = hasher

    async def execute(self, data: LoginModelDomain) -> HttpResponse:

        try:

            user = await self.repository.get_by_email(table_name=User, email=data.email)

            if not user:
                return HttpResponse(status_code=404, body={"message": "User not found"})

            if not await self.hasher.compare(data.password, user["password"]):
                return HttpResponse(
                    status_code=401, body={"message": "Invalid password"}
                )

            token = await self.authenticator.encode(UserModelDomain(**user))

            return HttpResponse(status_code=200, body={"token": token})

        except Exception as error:
            return HttpResponse(status_code=500, body={"Error": error})
