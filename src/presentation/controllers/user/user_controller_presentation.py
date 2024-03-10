from typing_extensions import List, TypeVar, Type, Generic
from fastapi import UploadFile
from pydantic import BaseModel
from src.domain.models.user_models_domain import ImageUpload
from src.domain.protocols.user_protocols_domain import UserDomainProtocol
from src.presentation.contracts.controller_contract_presentation import Controller
from src.presentation.types.http_types_presentation import HttpRequest, HttpResponse
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
        self, request: HttpRequest, files: List[UploadFile]
    ) -> HttpResponse:
        try:

            if not request.headers or not request.body:
                return HttpResponse(
                    status_code=400, body={"message": "Request not found"}
                )

            method = request.headers["method"]
            user = request.headers["user"]
            body = request.body

            file = files[0]
            image_upload = ImageUpload(
                filename=file.filename,
                mimetype=file.content_type,
                body=file.file.read(),
            ).model_dump()

            body["image_upload"] = image_upload

            schema_validator = await self.validator.validate(body, self.schema)

            if isinstance(schema_validator, list):
                return HttpResponse(status_code=422, body=schema_validator)

            response = await self.use_case.execute(
                data_user=schema_validator,
                user=user,
                method=method,
            )

            return HttpResponse(status_code=response.status_code, body=response.body)
        except Exception as e:
            return HttpResponse(status_code=500, body={"Error": e})

    async def execute_json(self, request: HttpRequest) -> HttpResponse:
        try:
            if not request.headers or not request.body:
                return HttpResponse(
                    status_code=400, body={"message": "Request not found"}
                )

            method = request.headers["method"]
            user = request.headers["user"]

            response = await self.use_case.execute(
                user=user,
                method=method,
            )

            return HttpResponse(status_code=response.status_code, body=response.body)
        except Exception as e:
            return HttpResponse(status_code=500, body={"Error": e})
