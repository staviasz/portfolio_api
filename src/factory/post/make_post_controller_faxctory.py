from src.configs.repository.client_repository_config import SessionLocal
from src.infra.pydantic.validator_schema_infra import ValidatorSchemaInfra
from src.infra.repository.implement.repository_infra import RepositoryInfra
from src.presentation.contracts.controller_contract_presentation import Controller
from src.presentation.controllers.post.post_controller_presentation import (
    PostControllerPresentation,
)
from src.presentation.validators.schemas.post_schema_presentation import (
    PostSchemaPresentation,
)
from src.use_case.implements.post.post_implements_use_case import PostUseCase


def make_post_controller() -> Controller:
    repository = RepositoryInfra(SessionLocal())
    use_case = PostUseCase(repository=repository)
    validator = ValidatorSchemaInfra()
    schema = PostSchemaPresentation
    return PostControllerPresentation(
        schema=schema, use_case=use_case, validator=validator
    )
