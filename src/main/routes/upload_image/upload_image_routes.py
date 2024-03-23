from fastapi import APIRouter, File, Form, Header, Response, UploadFile
from fastapi.responses import JSONResponse
from src.adapters.rotes.route_adapter import adapt_router
from src.factory.middlewares.auth_middleware_factory import make_auth_middleware
from src.factory.upload_image.make_upload_image_controller_factory import (
    make_upload_image_controller,
)
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.presentation.types.http_types_presentation import HttpRequest


class UploadImageRoutes:
    def __init__(self, router: APIRouter, prefix: str):
        self._router = router
        self._prefix = prefix

    def routes_setup(self):

        @self._router.post(f"{self._prefix}")
        async def upload_image(
            authorization: str = Header(...),
            folder_name: str = Form(...),
            files: list[UploadFile] = File(...),
        ) -> Response:
            try:
                request = HttpRequest(
                    headers={"Authorization": authorization.split(" ")[1]},
                    body={"folder_name": folder_name},
                )

                adapt = await adapt_router(
                    controller=make_upload_image_controller(),
                    request=request,
                    middlewares={"auth": make_auth_middleware()},
                )

                return await adapt.adapt_with_files_form_data(
                    request=request, files=files
                )
            except ExceptionCustomPresentation as error:
                return JSONResponse(status_code=error.status_code, content=error.body)

        return self._router
