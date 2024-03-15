from typing_extensions import Dict

from src.adapters.rotes.fast_route_adapter import FastRouteAdapter
from src.presentation.contracts.controller_contract_presentation import Controller
from src.presentation.contracts.middleware_contract_presentation import (
    MiddlewareContract,
)
from src.presentation.types.http_types_presentation import HttpRequest


async def adapt_router(
    controller: Controller,
    request: HttpRequest | None = None,
    middlewares: Dict[str, MiddlewareContract] | None = None,
) -> FastRouteAdapter:
    try:
        results_middleware = []

        if not middlewares:
            return FastRouteAdapter(controller)

        if request and middlewares:
            for key, middleware in middlewares.items():
                result_middleware = await middleware.execute(request=request)
                results_middleware.append(result_middleware)

        return FastRouteAdapter(controller, *results_middleware)
    except Exception as error:
        raise error
