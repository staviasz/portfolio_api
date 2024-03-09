from src.use_case.protocols.jwt.decode_jwt_protocol_use_case import (
    JwtDecodeProtocolUseCase,
)
from src.use_case.protocols.jwt.encode_jwt_protocol_use_case import (
    JwtEncodeProtocolUseCase,
)


class JwtProtocolUseCase(JwtEncodeProtocolUseCase, JwtDecodeProtocolUseCase):
    pass
