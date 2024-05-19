from typing_extensions import List, TypeVar, Type, Generic
from fastapi import UploadFile
from pydantic import BaseModel
from src.domain.protocols.user_protocols_domain import UserDomainProtocol
from src.presentation.contracts.controller_contract_presentation import Controller
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.presentation.types.http_types_presentation import HttpRequest, HttpResponse
from src.presentation.types.image_upload_type_presentation import ImageUpload
from src.use_case.protocols.pydantic.validation_schema_pydantic_protocol_use_case import (
    ValidationSchemaProtocolUseCase,
)

TSchema = TypeVar("TSchema", bound=BaseModel)


class UserControllerPresentation(Controller, Generic[TSchema]):

    def __init__(
        self,
        validator: ValidationSchemaProtocolUseCase,
        schema: Type[TSchema],
        use_case: UserDomainProtocol,
    ):
        self.validator = validator
        self.schema = schema
        self.use_case = use_case

    async def execute_with_files_form_data(
        self,
        request: HttpRequest | None = None,
        files: List[UploadFile] | None = None,
        *args,
        **kwargs
    ) -> HttpResponse:

        if not request and not files:
            return HttpResponse(
                status_code=400, body={"message": "Request or files must be provided"}
            )

        try:
            user = None
            body = request.body if request and request.body else {}
            method = (
                request.headers.get("method") if request and request.headers else None
            )

            args = kwargs.get("args", None)
            if args:
                user = args[0]

            if files and files[0]:
                file = files[0]
                body["image_upload"] = ImageUpload(
                    filename=file.filename,
                    mimetype=file.content_type,
                    body=file.file.read(),
                ).model_dump()

            schema_validator = await self.validator.validate(body, self.schema)

            if isinstance(schema_validator, list):
                return HttpResponse(status_code=422, body=schema_validator)

            response = await self.use_case.execute(
                user=user,
                data_user=schema_validator,
                method=method,
            )

            return HttpResponse(status_code=response.status_code, body=response.body)
        except ExceptionCustomPresentation as error:
            return HttpResponse(status_code=error.status_code, body=error.body)

    async def execute_json(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        try:
            method = None
            user = None
            args = kwargs.get("args", None)

            if args:
                user = args[0]

            method = request.headers.get("method") if request.headers else None
            user_id = request.params.get("user_id") if request.params else None

            response = await self.use_case.execute(
                user=user,
                method=method,
                user_id=user_id,
            )

            return HttpResponse(status_code=response.status_code, body=response.body)
        except ExceptionCustomPresentation as error:
            return HttpResponse(status_code=error.status_code, body=error.body)
