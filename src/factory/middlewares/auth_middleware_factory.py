from src.presentation.contracts.middleware_contract_presentation import (
    MiddlewareContract,
)
from src.presentation.middlewares.auth_user_middleware import AuthMiddleware
from src.infra.jwt.auth_jwt_infra import AuthJwtInfra


def make_auth_middleware() -> MiddlewareContract:
    authenticator = AuthJwtInfra()
    return AuthMiddleware(autenticator=authenticator)
