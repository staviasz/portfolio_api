from typing_extensions import Type, List
from src.presentation.errors.error_schema_presentation import ErrorSchema, error_schema
from src.use_case.protocols.pydantic.validation_schema_pydantic_protocol_use_case import (
    T,
    ValidationSchemaProtocolUseCase,
)


class ValidatorSchemaInfra(ValidationSchemaProtocolUseCase):
    async def validate(self, data: dict, schema: Type[T]) -> T | List[ErrorSchema]:
        try:
            return schema(**data)
        except Exception as e:
            return error_schema(str(e))
