from typing_extensions import Protocol


class BycryptCompareProtocolUseCase(Protocol):
    async def compare(self, password: str, Hash_password: str) -> bool: ...
