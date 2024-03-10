from typing_extensions import Protocol, TypeVar, Type, List

from pydantic import BaseModel

from src.presentation.errors.error_schema_presentation import ErrorSchema

T = TypeVar("T", bound=BaseModel)


class ValidationSchemaProtocolUseCase(Protocol):

    async def validate(self, data: dict, schema: Type[T]) -> T | List[ErrorSchema]: ...
