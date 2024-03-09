from src.use_case.protocols.bycript.compare_bycript_protocol_use_case import (
    BycryptCompareProtocolUseCase,
)

from src.use_case.protocols.bycript.hash_bycript_protocol_use_case import (
    BycryptHashProtocolUseCase,
)


class BycryptProtocolUseCase(BycryptHashProtocolUseCase, BycryptCompareProtocolUseCase):
    pass
