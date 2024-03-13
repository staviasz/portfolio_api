from fastapi import APIRouter, File, Form, Header, Response, UploadFile
from fastapi.responses import JSONResponse

from src.adapters.rotes.route_adapter import adapt_router
from src.factory.middlewares.auth_middleware_factory import make_auth_middleware
from src.factory.user.user_controller_factory import make_user_controller
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
        ) -> Response:

            try:
                request = HttpRequest(
                    body={
                        "name": name,
                        "email": email,
                        "password": password,
                        "description": description,
                        "contact_description": contact_description,
                    }
                )

                adapt = adapt_router(make_user_controller("create"))

                return await adapt.adapt_with_files_form_data(
                    request=request, files=[file]
                )

            except Exception as error:
                return JSONResponse(status_code=500, content=error)

        @self._router.get(f"{self.prefix}")
        async def get_user():
            adapt = adapt_router(make_user_controller())
            await adapt.adapt_json()
            return

        @self._router.get(f"{self.prefix}")
        async def get_all_user():
            return

        @self._router.put(f"{self.prefix}")
        async def update_user(
            authorization: str = Header(...),
            file: UploadFile = File(None),
            name: str = Form(None),
            email: str = Form(None),
            password: str = Form(None),
            description: str = Form(None),
            contact_description: str = Form(None),
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
                    },
                )

                adapt = adapt_router(
                    controller=make_user_controller(),
                    request=request,
                    middlewares={"auth": make_auth_middleware()},
                )

                return await adapt.adapt_with_files_form_data(
                    request=request, files=[file]
                )

            except Exception as error:
                return JSONResponse(status_code=500, content=error)

        @self._router.delete(f"{self.prefix}")
        async def delete_user():
            return

        return self._router
