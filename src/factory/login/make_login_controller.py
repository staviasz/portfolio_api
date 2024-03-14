from src.configs.repository.client_repository_config import SessionLocal
from src.infra.bycript.hasher_bycript_infra import HasherInfra
from src.infra.jwt.auth_jwt_infra import AuthJwtInfra
from src.infra.pydantic.validator_schema_infra import ValidatorSchemaInfra
from src.infra.repository.implement.repository_infra import RepositoryInfra
from src.presentation.contracts.controller_contract_presentation import Controller
from src.presentation.controllers.login.login_controller_presentation import (
    LoginControllerPresentation,
)
from src.presentation.validators.schemas.login_schema_presentation import (
    LoginSchemaPresentation,
)
from src.use_case.implements.login.login_implementation_use_case import loginUseCase


def make_login_controller() -> Controller:

    repository = RepositoryInfra(SessionLocal())
    authenticator = AuthJwtInfra()
    hasher = HasherInfra()

    use_case = loginUseCase(
        authenticator=authenticator, hasher=hasher, repository=repository
    )
    validator = ValidatorSchemaInfra()
    schema = LoginSchemaPresentation

    return LoginControllerPresentation(
        validator=validator, schema=schema, use_case=use_case
    )
