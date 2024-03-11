from typing_extensions import Literal
from src.configs.repository.client_repository_config import SessionLocal
from src.configs.aws.client_aws_config import s3_client
from src.infra.aws.aws_infra import AwsInfra
from src.infra.bycript.hasher_bycript_infra import HasherInfra
from src.infra.repository.implement.repository_infra import RepositoryInfra
from src.presentation.contracts.controller_contract_presentation import Controller
from src.presentation.controllers.user.user_controller_presentation import (
    UserControllerPresentation,
)
from src.infra.pydantic.validator_schema_infra import ValidatorSchemaInfra
from src.presentation.validators.schemas.user_create_schema_presentation import (
    UserCreateSchema,
)
from src.presentation.validators.schemas.user_update_schema_presentation import (
    UserUpdateSchema,
)
from src.use_case.implements.user.user_implement_use_case import UserUseCase


def make_user_controller(
    action: Literal["create", "update"] | None = None
) -> Controller:
    repository = RepositoryInfra(SessionLocal())
    bucket = AwsInfra(s3_client)
    hasher = HasherInfra()

    use_case = UserUseCase(repository=repository, bucket=bucket, hasher=hasher)
    validator = ValidatorSchemaInfra()
    schema = UserCreateSchema if action == "create" else UserUpdateSchema

    return UserControllerPresentation(
        validator=validator, schema=schema, use_case=use_case
    )
