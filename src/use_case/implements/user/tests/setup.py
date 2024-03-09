from typing_extensions import Any
from unittest.mock import Mock
from src.use_case.implements.user.user_implement_use_case import UserUseCase
from src.use_case.protocols.aws.aws_protocol_use_case import AwsProtocolUseCase
from src.use_case.protocols.bycript.bycript_protocol_use_case import (
    BycryptProtocolUseCase,
)
from src.use_case.protocols.repository.repository_protocol_use_case import (
    RepositoryProtocolUseCase,
)

repository = Mock(spec_set=RepositoryProtocolUseCase)
bucket = Mock(spec_set=AwsProtocolUseCase)
hasher = Mock(spec_set=BycryptProtocolUseCase)
use_case = UserUseCase(
    repository=repository,
    bucket=bucket,
    hasher=hasher,
)

data_user: dict[str, Any] = {
    "name": "test",
    "email": "test",
    "password": "test",
    "image_upload": {
        "filename": "teste.txt",
        "body": b"teste",
        "mimetype": "text/plain",
    },
    "description": "test",
    "contact_description": "teste",
}
