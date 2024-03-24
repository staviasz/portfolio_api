from typing_extensions import Type, TypeVar, List
from fastapi import UploadFile
from pydantic import BaseModel
from src.domain.models.user_models_domain import UserModelDomain
from src.domain.protocols.post_protocols_domain import PostDomainProtocol
from src.presentation.contracts.controller_contract_presentation import Controller
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.presentation.types.http_types_presentation import HttpRequest, HttpResponse
from src.use_case.protocols.pydantic.validation_schema_pydantic_protocol_use_case import (
    ValidationSchemaProtocolUseCase,
)

TSchema = TypeVar("TSchema", bound=BaseModel)


class PostControllerPresentation(Controller):
    def __init__(
        self,
        validator: ValidationSchemaProtocolUseCase,
        schema: Type[TSchema],
        use_case: PostDomainProtocol,
    ):
        self.validator = validator
        self.schema = schema
        self.use_case = use_case

    async def execute_json(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        try:
            user = None
            args = kwargs.get("args", None)
            if args:
                user = args[0]
                user = UserModelDomain(**user)

            post_id = (
                request.params.get("post_id") if request and request.params else None
            )
            method = (
                request.headers.get("method") if request and request.headers else None
            )
            filters = (
                request.query.get("filters") if request and request.query else None
            )

            if not request.body:
                return HttpResponse(
                    status_code=400,
                    body={"message": "Request body must be provided"},
                )

            schema_validator = await self.validator.validate(request.body, self.schema)
            if isinstance(schema_validator, list):
                return HttpResponse(status_code=422, body=schema_validator)

            response = await self.use_case.execute(
                data=schema_validator,
                user=user,
                method=method,
                post_id=post_id,
                filters=filters,
            )

            return HttpResponse(
                status_code=response.status_code,
                body=response.body,
            )
        except ExceptionCustomPresentation as error:
            return HttpResponse(status_code=error.status_code, body=error.body)

    async def execute_with_files_form_data(
        self,
        request: HttpRequest | None,
        files: List[UploadFile] | None,
        *args,
        **kwargs
    ) -> HttpResponse:
        return HttpResponse(status_code=501, body={"message": "Not implemented"})
