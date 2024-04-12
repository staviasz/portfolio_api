from src.domain.models.techs_models_domain import TechsModelsDomain
from src.domain.protocols.use_case_protocol_domain import DomainProtocol
from src.infra.repository.models.tech_model_repository_infra import Tech
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.presentation.types.http_types_presentation import HttpResponse
from src.use_case.protocols.repository.repository_protocol_use_case import (
    RepositoryProtocolUseCase,
)


class TechUsaCase(DomainProtocol):

    def __init__(self, repository: RepositoryProtocolUseCase) -> None:
        self.repository = repository

    async def execute(self, *args, **kwargs) -> HttpResponse:
        try:
            techs = await self.repository.get_all(table_name=Tech)

            response = [TechsModelsDomain(**techs).model_dump() for techs in techs]

            return HttpResponse(status_code=200, body=response)
        except ExceptionCustomPresentation as error:
            return HttpResponse(status_code=error.status_code, body=error.body)
