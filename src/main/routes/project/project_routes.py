from fastapi import APIRouter, File, Form, Header, Request, Response, UploadFile
from fastapi.responses import JSONResponse
from pydantic import HttpUrl

from src.adapters.rotes.route_adapter import adapt_router
from src.factory.middlewares.auth_middleware_factory import make_auth_middleware
from src.factory.project.make_project_controller_factory import make_project_controller
from src.presentation.errors.unautorized_exception_presentation import (
    UnauthorizedException,
)
from src.presentation.types.http_types_presentation import HttpRequest


class ProjectRoutes:
    def __init__(self, _router: APIRouter, prefix: str):
        self._router = _router
        self.prefix = prefix

    def routes_setup(self):
        @self._router.post(f"{self.prefix}")
        async def create_project(
            authorization: str = Header(...),
            files: list[UploadFile] = File(...),
            name: str = Form(...),
            description: str = Form(...),
            link_deploy: HttpUrl | None = Form(None),
            link_code: HttpUrl = Form(...),
        ) -> Response:
            try:
                new_request = HttpRequest(
                    headers={
                        "Authorization": authorization.split(" ")[1],
                    },
                    body={
                        "name": name,
                        "description": description,
                        "link_deploy": link_deploy,
                        "link_code": link_code,
                    },
                )

                adapt = await adapt_router(
                    controller=make_project_controller("create"),
                    request=new_request,
                    middlewares={"auth": make_auth_middleware()},
                )

                return await adapt.adapt_with_files_form_data(
                    request=new_request, files=files
                )
            except UnauthorizedException as error:
                return JSONResponse(status_code=401, content=error.__dict__)

            except Exception as error:
                return JSONResponse(status_code=500, content=error)

        @self._router.get(f"{self.prefix}/{{project_id}}")
        async def get_projects(
            project_id: int, request: Request, authorization: str = Header(...)
        ) -> Response:
            try:
                new_request = HttpRequest(
                    params={"project_id": project_id},
                    headers={
                        "Authorization": authorization.split(" ")[1],
                        "method": request.method,
                    },
                )
                adapt = await adapt_router(
                    request=new_request,
                    controller=make_project_controller(),
                    middlewares={"auth": make_auth_middleware()},
                )
                return await adapt.adapt_json(new_request)
            except UnauthorizedException as error:
                return JSONResponse(status_code=401, content=error.__dict__)

            except Exception as error:
                return JSONResponse(status_code=500, content=error)

        @self._router.put(f"{self.prefix}/{{project_id}}")
        async def update_project(
            project_id: int,
            request: Request,
            authorization: str = Header(...),
            files: list[UploadFile] = File(None),
            name: str | None = Form(None),
            description: str | None = Form(None),
            link_deploy: HttpUrl | None = Form(None),
            link_code: HttpUrl | None = Form(None),
        ) -> Response:
            try:
                new_request = HttpRequest(
                    params={"project_id": project_id},
                    headers={
                        "Authorization": authorization.split(" ")[1],
                        "method": request.method,
                    },
                    body={
                        "name": name,
                        "description": description,
                        "link_deploy": link_deploy,
                        "link_code": link_code,
                    },
                )

                adapt = await adapt_router(
                    controller=make_project_controller(),
                    request=new_request,
                    middlewares={"auth": make_auth_middleware()},
                )

                return await adapt.adapt_with_files_form_data(
                    request=new_request, files=files
                )
            except UnauthorizedException as error:
                return JSONResponse(status_code=401, content=error.__dict__)

            except Exception as error:
                return JSONResponse(status_code=500, content=error)

        @self._router.get(f"{self.prefix}")
        async def get_all_projects(request: Request, authorization: str = Header(...)):
            try:

                new_request = HttpRequest(
                    headers={
                        "Authorization": authorization.split(" ")[1],
                    },
                )

                adapt = await adapt_router(
                    controller=make_project_controller(),
                    request=new_request,
                    middlewares={"auth": make_auth_middleware()},
                )
                return await adapt.adapt_json(new_request)

            except UnauthorizedException as error:
                return JSONResponse(status_code=401, content=error.__dict__)

            except Exception as error:
                return JSONResponse(status_code=500, content=error)

        @self._router.delete(f"{self.prefix}/{{project_id}}")
        async def delete_project(
            project_id: int, request: Request, authorization: str = Header(...)
        ) -> Response:
            try:
                new_request = HttpRequest(
                    params={"project_id": project_id},
                    headers={
                        "Authorization": authorization.split(" ")[1],
                        "method": request.method,
                    },
                )
                adapt = await adapt_router(
                    controller=make_project_controller(),
                    request=new_request,
                    middlewares={"auth": make_auth_middleware()},
                )
                return await adapt.adapt_json(new_request)
            except UnauthorizedException as error:
                return JSONResponse(status_code=401, content=error.__dict__)

        return self._router
