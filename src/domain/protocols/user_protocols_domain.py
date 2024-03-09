from typing_extensions import Literal, Protocol

from src.domain.models.user_models_domain import (
    UserModelCreateDomain,
    UserModelDomain,
    UserModelUpdateDomain,
)
from src.presentation.types.http_types_presentation import HttpResponse


class UserDomainProtocol(Protocol):
    async def add_user(self, user: UserModelCreateDomain) -> HttpResponse: ...

    async def edit_user(
        self, user: UserModelDomain, data_user: UserModelUpdateDomain
    ) -> HttpResponse: ...

    async def get_user(self, user_id: int) -> HttpResponse: ...

    async def get_all_users(self) -> HttpResponse: ...

    async def delete_user(self, user_id: int) -> HttpResponse: ...

    async def execute(
        self,
        data_user: UserModelCreateDomain | UserModelUpdateDomain | None = None,
        user: UserModelDomain | None = None,
        method: Literal["POST", "GET", "PUT", "DELETE"] | None = None,
    ) -> HttpResponse:
        if data_user and isinstance(data_user, UserModelCreateDomain):
            return await self.add_user(data_user)

        elif (
            data_user
            and isinstance(data_user, UserModelUpdateDomain)
            and user
            and isinstance(user, UserModelDomain)
        ):
            return await self.edit_user(user, data_user)

        elif user and method == "GET":
            return await self.get_user(user.id)

        elif user and method == "DELETE":
            return await self.delete_user(user.id)

        else:
            return await self.get_all_users()
