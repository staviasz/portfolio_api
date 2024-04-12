from fastapi import APIRouter, File, Form, Header, Request, Response, UploadFile
from fastapi.responses import JSONResponse
from pydantic import HttpUrl

from src.adapters.rotes.route_adapter import adapt_router
from src.domain.models.project_models_domain import ProjectModelDomain
from src.factory.middlewares.auth_middleware_factory import make_auth_middleware
from src.factory.project.make_project_controller_factory import make_project_controller
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)

from src.presentation.types.http_types_presentation import HttpRequest


class ProjectRoutes:
    def __init__(self, _router: APIRouter, prefix: str):
        self._router = _router
        self.prefix = prefix

    def routes_setup(self):
        @self._router.post(
            f"{self.prefix}", tags=["Project"], response_model=ProjectModelDomain
        )
        async def create_project(
            authorization: str = Header(...),
            files: list[UploadFile] = File(...),
            name: str = Form(...),
            description: str = Form(...),
            link_deploy: HttpUrl | None = Form(None),
            link_code: HttpUrl = Form(...),
            techs: list[int] = Form(None),
        ) -> Response:
            """
            Args:\n
                {
                    name: str
                    description: str
                    link_deploy: Optional[HttpUrl] = None
                    link_code: HttpUrl
                    images_uploads: list[ImageUpload]
                    techs: Optional[list[int]] = None
                }
            """
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
                        "techs": techs,
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

            except ExceptionCustomPresentation as error:
                return JSONResponse(status_code=error.status_code, content=error.body)

        @self._router.get(
            f"{self.prefix}/{{project_id}}",
            tags=["Project"],
            response_model=ProjectModelDomain,
        )
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

            except ExceptionCustomPresentation as error:
                return JSONResponse(status_code=error.status_code, content=error.body)

        @self._router.put(
            f"{self.prefix}/{{project_id}}",
            tags=["Project"],
            response_model=ProjectModelDomain,
        )
        async def update_project(
            project_id: int,
            request: Request,
            authorization: str = Header(...),
            files: list[UploadFile] = File(None),
            name: str | None = Form(None),
            description: str | None = Form(None),
            link_deploy: HttpUrl | None = Form(None),
            link_code: HttpUrl | None = Form(None),
            techs: list[int] = Form(None),
        ) -> Response:
            """
            Args:\n
                {
                    name: Optional[str] = None
                    description: Optional[str] = None
                    link_deploy: Optional[HttpUrl] = None
                    link_code: Optional[HttpUrl] = None
                    images_uploads: Optional[list[ImageUpload]] = None
                    techs: Optional[list[int]] = None
                }
            """
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
                        "techs": techs,
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
            except ExceptionCustomPresentation as error:
                return JSONResponse(status_code=error.status_code, content=error.body)

        @self._router.get(
            f"{self.prefix}", tags=["Project"], response_model=ProjectModelDomain
        )
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

            except ExceptionCustomPresentation as error:
                return JSONResponse(status_code=error.status_code, content=error.body)

        @self._router.delete(
            f"{self.prefix}/{{project_id}}",
            tags=["Project"],
            response_model=ProjectModelDomain,
        )
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

            except ExceptionCustomPresentation as error:
                return JSONResponse(status_code=error.status_code, content=error.body)

        return self._router
