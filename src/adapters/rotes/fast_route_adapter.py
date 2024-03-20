from typing_extensions import List
from fastapi import UploadFile
from fastapi.responses import JSONResponse
from src.presentation.contracts.controller_contract_presentation import Controller
from src.presentation.types.http_types_presentation import HttpRequest


class FastRouteAdapter:
    def __init__(self, controller: Controller, *args, **kwargs) -> None:
        self.controller = controller
        self.args = args
        self.kwargs = kwargs

    async def adapt_with_files_form_data(
        self, request: HttpRequest, files: List[UploadFile] | None
    ) -> JSONResponse:

        response_api = await self.controller.execute_with_files_form_data(
            request=request, files=files, args=self.args, kwargs=self.kwargs
        )

        return JSONResponse(
            status_code=response_api.status_code,
            content=response_api.body,
        )

    async def adapt_json(self, request: HttpRequest) -> JSONResponse:

        response_api = await self.controller.execute_json(
            request=request, args=self.args, kwargs=self.kwargs
        )

        return JSONResponse(
            status_code=response_api.status_code,
            content=response_api.body,
        )
