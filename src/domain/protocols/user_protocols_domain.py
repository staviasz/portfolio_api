from typing_extensions import Literal, Protocol, TypeVar

from pydantic import BaseModel

from src.domain.models.user_models_domain import (
    UserModelCreateDomain,
    UserModelUpdateDomain,
)
from src.domain.protocols.use_case_protocol_domain import DomainProtocol
from src.presentation.types.http_types_presentation import HttpResponse

T = TypeVar("T", bound=BaseModel)


class UserDomainProtocol(DomainProtocol, Protocol):
    async def add_user(self, user: UserModelCreateDomain) -> HttpResponse: ...

    async def edit_user(
        self, user: dict, data_user: UserModelUpdateDomain
    ) -> HttpResponse: ...

    async def get_user(self, user: dict) -> HttpResponse: ...

    async def get_all_users(self) -> HttpResponse: ...

    async def delete_user(self, user_id: int) -> HttpResponse: ...

    async def execute(
        self,
        data_user: T | None = None,
        user: dict | None = None,
        method: Literal["POST", "GET", "PUT", "DELETE"] | None = None,
    ) -> HttpResponse:

        if data_user and isinstance(data_user, UserModelCreateDomain):
            return await self.add_user(data_user)

        elif data_user and isinstance(data_user, UserModelUpdateDomain) and user:
            return await self.edit_user(user, data_user)

        elif user and method == "GET":
            return await self.get_user(user)

        elif user and method == "DELETE":
            return await self.delete_user(user["id"])

        elif not method:
            return await self.get_all_users()

        return HttpResponse(status_code=501, body={"Error": "Method not implemented"})
