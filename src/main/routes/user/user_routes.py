from fastapi import APIRouter, File, Form, Header, Request, Response, UploadFile
from fastapi.responses import JSONResponse

from src.adapters.rotes.route_adapter import adapt_router
from src.factory.middlewares.auth_middleware_factory import make_auth_middleware
from src.factory.user.user_controller_factory import make_user_controller
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)

from src.presentation.types.http_types_presentation import HttpRequest


class UserRoutes:
    def __init__(self, _router: APIRouter, prefix: str):
        self._router = _router
        self.prefix = prefix

    def routes_setup(self):
        @self._router.post(f"{self.prefix}")
        async def add_user(
            file: UploadFile = File(...),
            name: str = Form(...),
            email: str = Form(...),
            password: str = Form(...),
            description: str = Form(...),
            contact_description: str = Form(...),
            techs: list[int] = Form(None),
        ) -> Response:

            try:
                request = HttpRequest(
                    body={
                        "name": name,
                        "email": email,
                        "password": password,
                        "description": description,
                        "contact_description": contact_description,
                        "techs": techs,
                    }
                )

                adapt = await adapt_router(make_user_controller("create"))

                return await adapt.adapt_with_files_form_data(
                    request=request, files=[file]
                )

            except ExceptionCustomPresentation as error:
                return JSONResponse(status_code=error.status_code, content=error.body)

        @self._router.get(f"{self.prefix}/profile")
        async def get_user(req: Request, authorization: str = Header(...)):
            try:
                request = HttpRequest(
                    headers={
                        "Authorization": authorization.split(" ")[1],
                        "method": req.method,
                    }
                )
                adapt = await adapt_router(
                    request=request,
                    controller=make_user_controller(),
                    middlewares={"auth": make_auth_middleware()},
                )
                return await adapt.adapt_json(request)
            except ExceptionCustomPresentation as error:
                return JSONResponse(status_code=error.status_code, content=error.body)

        @self._router.get(f"{self.prefix}")
        async def get_all_user(authorization: str = Header(...)):
            try:

                request = HttpRequest(
                    headers={
                        "Authorization": authorization.split(" ")[1],
                    }
                )
                adapt = await adapt_router(
                    request=request,
                    controller=make_user_controller(),
                    middlewares={"auth": make_auth_middleware()},
                )
                return await adapt.adapt_json(request)
            except ExceptionCustomPresentation as error:
                return JSONResponse(status_code=error.status_code, content=error.body)

        @self._router.put(f"{self.prefix}")
        async def update_user(
            authorization: str = Header(...),
            file: UploadFile = File(None),
            name: str = Form(None),
            email: str = Form(None),
            password: str = Form(None),
            description: str = Form(None),
            contact_description: str = Form(None),
            techs: list[int] = Form(None),
        ) -> Response:

            try:

                request = HttpRequest(
                    headers={
                        "Authorization": authorization.split(" ")[1],
                    },
                    body={
                        "name": name,
                        "email": email,
                        "password": password,
                        "description": description,
                        "contact_description": contact_description,
                        "techs": techs,
                    },
                )

                adapt = await adapt_router(
                    controller=make_user_controller(),
                    request=request,
                    middlewares={"auth": make_auth_middleware()},
                )

                return await adapt.adapt_with_files_form_data(
                    request=request, files=[file]
                )

            except ExceptionCustomPresentation as error:
                return JSONResponse(status_code=error.status_code, content=error.body)

        @self._router.delete(f"{self.prefix}")
        async def delete_user(req: Request, authorization: str = Header(...)):

            try:
                request = HttpRequest(
                    headers={
                        "Authorization": authorization.split(" ")[1],
                        "method": req.method,
                    }
                )
                adapt = await adapt_router(
                    request=request,
                    controller=make_user_controller(),
                    middlewares={"auth": make_auth_middleware()},
                )
                return await adapt.adapt_json(request)

            except ExceptionCustomPresentation as error:
                return JSONResponse(status_code=error.status_code, content=error.body)

        return self._router
