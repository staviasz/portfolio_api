import bcrypt
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.use_case.protocols.bycript.bycript_protocol_use_case import (
    BycryptProtocolUseCase,
)


class HasherInfra(BycryptProtocolUseCase):
    async def hash(self, password: str) -> str:
        try:
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            return hashed_password.decode("utf-8")
        except Exception as error:
            raise ExceptionCustomPresentation(
                status_code=500,
                message="Errror in hashing password",
                type="Error Server",
                error=error.args,
            )

    async def compare(self, password: str, hash_password: str) -> bool:
        try:
            return bcrypt.checkpw(
                password.encode("utf-8"), hash_password.encode("utf-8")
            )
        except Exception as error:
            raise ExceptionCustomPresentation(
                status_code=500,
                message="Errror in comparing password",
                type="Error Server",
                error=error.args,
            )
