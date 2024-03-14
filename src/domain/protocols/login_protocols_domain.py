from typing_extensions import Protocol

from src.domain.models.login_models_domain import LoginModelDomain
from src.presentation.types.http_types_presentation import HttpResponse


class LoginDomainProtocol(Protocol):

    async def execute(self, data: LoginModelDomain) -> HttpResponse: ...
