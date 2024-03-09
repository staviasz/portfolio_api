from typing_extensions import Protocol


class BycryptHashProtocolUseCase(Protocol):
    async def hash(self, password: str) -> str: ...
