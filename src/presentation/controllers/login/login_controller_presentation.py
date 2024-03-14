from typing_extensions import TypeVar, Type, List
from fastapi import UploadFile
from pydantic import BaseModel
from src.domain.models.login_models_domain import LoginModelDomain
from src.domain.protocols.login_protocols_domain import LoginDomainProtocol
from src.presentation.contracts.controller_contract_presentation import Controller
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
        use_case: LoginDomainProtocol,
    ):
        self.validator = validator
        self.schema = schema
        self.use_case = use_case

    async def execute_json(self, request: HttpRequest) -> HttpResponse:
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

        except Exception as error:
            return HttpResponse(status_code=500, body={"Error": error})

    async def execute_with_files_form_data(
        self, request: HttpRequest, files: List[UploadFile]
    ) -> HttpResponse:
        return HttpResponse(status_code=500, body={"message": "Not implemented"})
