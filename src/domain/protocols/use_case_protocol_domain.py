from typing_extensions import Protocol

from src.presentation.types.http_types_presentation import HttpResponse


class DomainProtocol(Protocol):

    async def execute(self, *args, **kwargs) -> HttpResponse: ...
