from typing_extensions import Literal, Protocol

from src.domain.models.user_models_domain import (
    UserModelCreateDomain,
    UserModelUpdateDomain,
)
from src.presentation.types.http_types_presentation import HttpResponse


class UserDomainProtocol(Protocol):
    async def add_user(self, user: UserModelCreateDomain) -> HttpResponse: ...

    async def edit_user(
        self, user_id: int, user: UserModelUpdateDomain
    ) -> HttpResponse: ...

    async def get_user(self, user_id: int) -> HttpResponse: ...

    async def get_all_users(self) -> HttpResponse: ...

    async def delete_user(self, user_id: int) -> HttpResponse: ...

    async def execute(
        self,
        user: UserModelCreateDomain | UserModelUpdateDomain | None = None,
        user_id: int | None = None,
        method: Literal["POST", "GET", "PUT", "DELETE"] | None = None,
    ) -> HttpResponse:
        if user and isinstance(user, UserModelCreateDomain):
            return await self.add_user(user)

        elif user and isinstance(user, UserModelUpdateDomain) and user_id:
            return await self.edit_user(user_id, user)

        elif user_id and method == "GET":
            return await self.get_user(user_id)

        elif user_id and method == "DELETE":
            return await self.delete_user(user_id)

        else:
            return await self.get_all_users()
