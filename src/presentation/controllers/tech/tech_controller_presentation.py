from typing_extensions import List

from fastapi import UploadFile
from src.domain.protocols.use_case_protocol_domain import DomainProtocol
from src.presentation.contracts.controller_contract_presentation import Controller
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.presentation.types.http_types_presentation import HttpRequest, HttpResponse


class TechController(Controller):
    def __init__(self, use_case: DomainProtocol):
        self.use_case = use_case

    async def execute_json(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        try:
            return await self.use_case.execute()
        except ExceptionCustomPresentation as error:
            return HttpResponse(status_code=error.status_code, body=error.body)

    async def execute_with_files_form_data(
        self, request: HttpRequest, files: List[UploadFile] | None, *args, **kwargs
    ) -> HttpResponse:
        return HttpResponse(status_code=501, body="Not Implemented")
