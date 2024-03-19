from typing_extensions import Literal
from src.configs.aws.client_aws_config import s3_client
from src.configs.repository.client_repository_config import SessionLocal
from src.infra.aws.aws_infra import AwsInfra
from src.infra.pydantic.validator_schema_infra import ValidatorSchemaInfra
from src.infra.repository.implement.repository_infra import RepositoryInfra
from src.presentation.contracts.controller_contract_presentation import Controller
from src.presentation.controllers.projects.projects_controller_presentation import (
    ProjectsControllerPresentation,
)
from src.presentation.validators.schemas.project_create_schema_presentation import (
    ProjectCreateSchema,
)
from src.presentation.validators.schemas.project_update_schema_presentation import (
    ProjectUpdateSchema,
)
from src.use_case.implements.project.project_implements_use_case import ProjectUseCase


def make_project_controller(action: Literal["create"] | None = None) -> Controller:
    repository = RepositoryInfra(SessionLocal())
    bucket = AwsInfra(s3_client)
    use_case = ProjectUseCase(repository=repository, bucket=bucket)

    validator = ValidatorSchemaInfra()
    schema = ProjectCreateSchema if action == "create" else ProjectUpdateSchema
    return ProjectsControllerPresentation(
        validator=validator, schema=schema, use_case=use_case
    )
