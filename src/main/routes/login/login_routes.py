from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.adapters.rotes.route_adapter import adapt_router
from src.factory.login.make_login_controller import make_login_controller
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.presentation.types.http_types_presentation import HttpRequest


class LoginResponse(BaseModel):
    token: str


class LoginRoutes:
    def __init__(self, router: APIRouter):
        self._router = router

    def routes_setup(self):
        @self._router.post("/login", tags=["Login"], response_model=LoginResponse)
        async def login(request: Request) -> Response:
            """
            Args:\n
                {
                    email: str
                    password: str
                }
            """

            try:

                new_request = HttpRequest(body=await request.json())
                print(new_request)

                adapt = await adapt_router(make_login_controller())

                return await adapt.adapt_json(new_request)

            except ExceptionCustomPresentation as error:
                return JSONResponse(status_code=error.status_code, content=error.body)

        return self._router
