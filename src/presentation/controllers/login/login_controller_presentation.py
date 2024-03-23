from typing_extensions import TypeVar, Type, List
from fastapi import UploadFile
from pydantic import BaseModel
from src.domain.models.login_models_domain import LoginModelDomain
from src.domain.protocols.use_case_protocol_domain import DomainProtocol
from src.presentation.contracts.controller_contract_presentation import Controller
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.presentation.types.http_types_presentation import HttpRequest, HttpResponse

from src.use_case.protocols.pydantic.validation_schema_pydantic_protocol_use_case import (
    ValidationSchemaProtocolUseCase,
)

TSchema = TypeVar("TSchema", bound=BaseModel)


class LoginControllerPresentation(Controller):

    def __init__(
        self,
        validator: ValidationSchemaProtocolUseCase,
        schema: Type[TSchema],
        use_case: DomainProtocol,
    ):
        self.validator = validator
        self.schema = schema
        self.use_case = use_case

    async def execute_json(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        try:

            if request.body is None:
                return HttpResponse(status_code=400, body={"message": "Missing body"})

            data = await self.validator.validate(request.body, self.schema)

            if isinstance(data, list):
                return HttpResponse(status_code=422, body=data)

            response = await self.use_case.execute(
                LoginModelDomain(**data.model_dump())
            )

            return HttpResponse(status_code=response.status_code, body=response.body)

        except ExceptionCustomPresentation as error:
            return HttpResponse(status_code=error.status_code, body=error.body)

    async def execute_with_files_form_data(
        self, request: HttpRequest, files: List[UploadFile] | None, *args, **kwargs
    ) -> HttpResponse:
        return HttpResponse(status_code=501, body={"message": "Not implemented"})
