from src.infra.aws.aws_infra import AwsInfra
from src.infra.pydantic.validator_schema_infra import ValidatorSchemaInfra
from src.presentation.contracts.controller_contract_presentation import Controller
from src.presentation.controllers.upload_image.upload_image_controller_presentation import (
    UploadImageController,
)
from src.presentation.validators.schemas.upload_image_schema_presentation import (
    UploadImageSchema,
)
from src.use_case.implements.upload_image.upload_image_implements_use_case import (
    UploadImageUseCase,
)
from src.configs.aws.client_aws_config import s3_client


def make_upload_image_controller() -> Controller:
    bucket = AwsInfra(client=s3_client)
    use_case = UploadImageUseCase(bucket=bucket)

    validator = ValidatorSchemaInfra()
    schema = UploadImageSchema
    return UploadImageController(validator=validator, schema=schema, use_case=use_case)
