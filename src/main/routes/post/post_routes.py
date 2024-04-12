from typing import Optional
from fastapi import APIRouter, Header, Query, Request, Response
from fastapi.responses import JSONResponse

from src.adapters.rotes.route_adapter import adapt_router
from src.domain.models.post_models_domain import PostDomain
from src.factory.middlewares.auth_middleware_factory import make_auth_middleware
from src.factory.post.make_post_controller_faxctory import make_post_controller
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)

from src.presentation.types.http_types_presentation import HttpRequest


class PostRoutes:
    def __init__(self, _router: APIRouter, prefix: str):
        self._router = _router
        self.prefix = prefix

    def routes_setup(self):
        @self._router.post(f"{self.prefix}", tags=["Post"], response_model=PostDomain)
        async def create_post(
            request: Request, authorization: str = Header(...)
        ) -> Response:
            """
            Args:\n
                {
                    name: str
                    html: str
                    images_urls: Optional[list[HttpUrl]] = None
                    techs: Optional[list[int]] = None
                }
            """
            try:

                new_request = HttpRequest(
                    headers={
                        "Authorization": authorization.split(" ")[1],
                        "method": request.method,
                    },
                    body=await request.json(),
                )
                adapt = await adapt_router(
                    controller=make_post_controller(action="create"),
                    request=new_request,
                    middlewares={"auth": make_auth_middleware()},
                )

                return await adapt.adapt_json(request=new_request)

            except ExceptionCustomPresentation as error:
                return JSONResponse(status_code=error.status_code, content=error.body)
            except Exception as error:
                return JSONResponse(status_code=500, content={"message": error.args})

        @self._router.put(
            f"{self.prefix}/{{post_id}}", tags=["Post"], response_model=PostDomain
        )
        async def update_post(
            request: Request, post_id: int, authorization: str = Header(...)
        ) -> Response:
            """
            Args:\n
                {
                    name: Optional[str]
                    html: Optional[str]
                    images_urls: Optional[list[HttpUrl]] = None
                    techs: Optional[list[int]] = None
                }
            """
            try:
                new_request = HttpRequest(
                    headers={
                        "Authorization": authorization.split(" ")[1],
                        "method": request.method,
                    },
                    params={"post_id": post_id},
                    body=await request.json(),
                )
                adapt = await adapt_router(
                    controller=make_post_controller(),
                    request=new_request,
                    middlewares={"auth": make_auth_middleware()},
                )

                return await adapt.adapt_json(request=new_request)

            except ExceptionCustomPresentation as error:
                return JSONResponse(status_code=error.status_code, content=error.body)

        @self._router.get(
            f"{self.prefix}/{{post_id}}", tags=["Post"], response_model=PostDomain
        )
        async def get_post(
            post_id: int, request: Request, authorization: str = Header(...)
        ) -> Response:
            try:
                new_request = HttpRequest(
                    headers={
                        "Authorization": authorization.split(" ")[1],
                        "method": request.method,
                    },
                    params={"post_id": post_id},
                )
                adapt = await adapt_router(
                    controller=make_post_controller(),
                    request=new_request,
                    middlewares={"auth": make_auth_middleware()},
                )

                return await adapt.adapt_json(request=new_request)

            except ExceptionCustomPresentation as error:
                return JSONResponse(status_code=error.status_code, content=error.body)

        @self._router.get(f"{self.prefix}", tags=["Post"], response_model=PostDomain)
        async def get_posts(
            request: Request,
            authorization: str = Header(...),
            user_id: Optional[int] = Query(None),
        ) -> Response:
            try:
                new_request = HttpRequest(
                    headers={
                        "Authorization": authorization.split(" ")[1],
                        "method": request.method,
                    },
                    query={"filters": {"user_id": user_id}} if user_id else None,
                )
                adapt = await adapt_router(
                    controller=make_post_controller(),
                    request=new_request,
                    middlewares={"auth": make_auth_middleware()},
                )

                return await adapt.adapt_json(request=new_request)

            except ExceptionCustomPresentation as error:
                return JSONResponse(status_code=error.status_code, content=error.body)

        @self._router.delete(
            f"{self.prefix}/{{post_id}}", tags=["Post"], response_model=PostDomain
        )
        async def delete_post(
            post_id: int, request: Request, authorization: str = Header(...)
        ) -> Response:
            try:
                new_request = HttpRequest(
                    headers={
                        "Authorization": authorization.split(" ")[1],
                        "method": request.method,
                    },
                    params={"post_id": post_id},
                )
                adapt = await adapt_router(
                    controller=make_post_controller(),
                    request=new_request,
                    middlewares={"auth": make_auth_middleware()},
                )

                return await adapt.adapt_json(request=new_request)

            except ExceptionCustomPresentation as error:
                return JSONResponse(status_code=error.status_code, content=error.body)

        return self._router
