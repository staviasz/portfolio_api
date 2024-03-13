from typing_extensions import Protocol
from src.presentation.types.http_types_presentation import HttpRequest


class MiddlewareContract(Protocol):
    async def execute(self, request: HttpRequest) -> dict | None: ...
