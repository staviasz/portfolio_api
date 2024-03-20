from fastapi import UploadFile
from typing_extensions import Protocol, List
from src.presentation.types.http_types_presentation import HttpRequest, HttpResponse


class Controller(Protocol):
    async def execute_with_files_form_data(
        self, request: HttpRequest, files: List[UploadFile] | None, *args, **kwargs
    ) -> HttpResponse: ...

    async def execute_json(
        self, request: HttpRequest, *args, **kwargs
    ) -> HttpResponse: ...
