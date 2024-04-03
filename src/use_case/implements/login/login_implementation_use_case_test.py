from unittest.mock import Mock
import pytest

from src.domain.models.login_models_domain import LoginModelDomain
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.use_case.implements.login.login_implementation_use_case import loginUseCase
from src.use_case.protocols.bycript.bycript_protocol_use_case import (
    BycryptProtocolUseCase,
)
from src.use_case.protocols.jwt.jwt_protocol_use_case import JwtProtocolUseCase
from src.use_case.protocols.repository.repository_protocol_use_case import (
    RepositoryProtocolUseCase,
)


repository = Mock(spec_set=RepositoryProtocolUseCase)
authenticator = Mock(spec_set=JwtProtocolUseCase)
hasher = Mock(spec_set=BycryptProtocolUseCase)

use_case = loginUseCase(
    repository=repository, authenticator=authenticator, hasher=hasher
)

data = LoginModelDomain(email="email", password="password")

user = {
    "id": 1,
    "name": "teste",
    "email": "email",
    "password": "password",
    "description": "teste_description",
    "contact_description": "contact_description",
    "image_url": "image_url",
}


@pytest.mark.asyncio
class TestLoginUseCase:
    async def test_get_by_email_exception(self):
        repository.get_by_email.side_effect = ExceptionCustomPresentation(
            status_code=500, message="Error Email Server", type="Error Server"
        )

        response = await use_case.execute(data)

        assert response.status_code == 500
        assert response.body == {
            "message": "Error Email Server",
            "type": "Error Server",
        }

    async def test_get_by_email_not_found(self):
        repository.get_by_email.side_effect = lambda *args, **kwargs: None

        response = await use_case.execute(data)

        assert response.status_code == 404
        assert response.body["message"] == "User not found"

    async def test_get_by_email(self):
        repository.get_by_email.side_effect = lambda *args, **kwargs: user

        response = await use_case.execute(data)

        assert response.status_code == 200
        assert response.body["token"]

    async def test_hasher_exception(self):
        hasher.compare.side_effect = ExceptionCustomPresentation(
            status_code=500, message="Error Hasher Server", type="Error Server"
        )

        response = await use_case.execute(data)

        assert response.status_code == 500
        assert response.body == {
            "message": "Error Hasher Server",
            "type": "Error Server",
        }

    async def test_hasher_false(self):
        hasher.compare.side_effect = lambda *args, **kwargs: False

        response = await use_case.execute(data)

        assert response.status_code == 401
        assert response.body["message"] == "Invalid password"

    async def test_hasher(self):
        hasher.compare.side_effect = lambda *args, **kwargs: True

        response = await use_case.execute(data)

        assert response.status_code == 200
        assert response.body["token"]

    async def test_autenticator_exception(self):
        authenticator.encode.side_effect = ExceptionCustomPresentation(
            status_code=500, message="Error Authenticator Server", type="Error Server"
        )

        response = await use_case.execute(data)

        assert response.status_code == 500
        assert response.body == {
            "message": "Error Authenticator Server",
            "type": "Error Server",
        }

    async def test_authenticator_success(self):
        authenticator.encode.side_effect = lambda *args, **kwargs: "token"

        response = await use_case.execute(data)

        assert response.status_code == 200
        assert response.body["token"] == "token"
