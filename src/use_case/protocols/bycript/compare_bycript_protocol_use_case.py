from typing_extensions import Protocol


class BycryptCompareProtocolUseCase(Protocol):
    async def compare(self, password: str, hash_password: str) -> bool: ...
