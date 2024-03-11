import bcrypt
from src.use_case.protocols.bycript.bycript_protocol_use_case import (
    BycryptProtocolUseCase,
)


class HasherInfra(BycryptProtocolUseCase):
    async def hash(self, password: str) -> str:
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        return hashed_password.decode("utf-8")

    async def compare(self, password: str, hash_password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hash_password.encode("utf-8"))
