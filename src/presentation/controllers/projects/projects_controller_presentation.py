from typing_extensions import List, TypeVar, Type
from fastapi import UploadFile
from pydantic import BaseModel
from src.domain.models.user_models_domain import UserModelDomain
from src.domain.protocols.project_protocols_domain import ProjectDomainProtocol
from src.presentation.contracts.controller_contract_presentation import Controller
from src.presentation.types.http_types_presentation import HttpRequest, HttpResponse
from src.presentation.types.image_upload_type_presentation import ImageUpload
from src.use_case.protocols.pydantic.validation_schema_pydantic_protocol_use_case import (
    ValidationSchemaProtocolUseCase,
)


TSchema = TypeVar("TSchema", bound=BaseModel)


class ProjectsControllerPresentation(Controller):

    def __init__(
        self,
        validator: ValidationSchemaProtocolUseCase,
        schema: Type[TSchema],
        use_case: ProjectDomainProtocol,
    ):
        self.validator = validator
        self.schema = schema
        self.use_case = use_case

    async def execute_with_files_form_data(
        self, request: HttpRequest, files: List[UploadFile], *args, **kwargs
    ) -> HttpResponse:
        if not request and not files:
            return HttpResponse(
                status_code=400, body={"message": "Request or files must be provided"}
            )
        try:
            user = None
            body = request.body if request and request.body else {}
            project_id = (
                request.params.get("id") if request and request.params else None
            )
            method = (
                request.headers.get("method") if request and request.headers else None
            )

            args = kwargs.get("args", None)
            if args:
                user = args[0]
                user = UserModelDomain(**user)

            if files:
                images_urls = []
                for file in files:
                    images_urls.append(
                        ImageUpload(
                            filename=file.filename,
                            mimetype=file.content_type,
                            body=file.file.read(),
                        ).model_dump()
                    )
                body["images_uploads"] = images_urls

            schema_validator = await self.validator.validate(body, self.schema)
            if isinstance(schema_validator, list):
                return HttpResponse(status_code=422, body=schema_validator)

            response = await self.use_case.execute(
                data=schema_validator,
                user=user,
                method=method,
                project_id=project_id,
            )

            return HttpResponse(status_code=response.status_code, body=response.body)
        except Exception as error:
            return HttpResponse(status_code=500, body={"Error": error})

    async def execute_json(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        try:
            project_id = (
                request.params.get("id") if request and request.params else None
            )
            method = (
                request.headers.get("method") if request and request.headers else None
            )

            response = await self.use_case.execute(project_id=project_id, method=method)

            return HttpResponse(
                status_code=200,
                body=response.body,
            )
        except Exception as error:
            return HttpResponse(status_code=500, body={"Error": error})
