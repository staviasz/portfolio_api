from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse

from src.adapters.rotes.route_adapter import adapt_router
from src.factory.tech.make_tech_factory import make_tech_factory
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.presentation.types.http_types_presentation import HttpRequest


class TechRoutes:
    def __init__(self, _router: APIRouter, prefix: str):
        self._router = _router
        self.prefix = prefix

    def routes_setup(self):
        @self._router.get(f"{self.prefix}", tags=["Tech"])
        async def get_all() -> Response:
            try:
                adapter = await adapt_router(make_tech_factory())

                return await adapter.adapt_json(HttpRequest())
            except ExceptionCustomPresentation as error:
                return JSONResponse(status_code=error.status_code, content=error.body)

        return self._router
