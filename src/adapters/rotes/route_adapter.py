from typing_extensions import Dict

from src.adapters.rotes.fast_route_adapter import FastRouteAdapter
from src.presentation.contracts.controller_contract_presentation import Controller


def adapt_router(
    controller: Controller, middlewares: Dict | None = None
) -> FastRouteAdapter:
    results_middleware = []

    if middlewares:
        for key, middleware in middlewares.items():
            result_middleware = middleware.execute()
            dict_ = {key: result_middleware}
            results_middleware.append(dict_)

    return FastRouteAdapter(controller, **results_middleware)
