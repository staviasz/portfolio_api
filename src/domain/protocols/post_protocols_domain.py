from typing_extensions import Literal, TypeVar, Protocol
from pydantic import BaseModel
from src.domain.models.post_models_domain import (
    PostCreateModelDomain,
    PostUpdatesModelDomain,
)
from src.domain.models.user_models_domain import UserModelDomain

from src.presentation.types.http_types_presentation import HttpResponse

TSchema = TypeVar("TSchema", bound=BaseModel)


class PostDomainProtocol(Protocol):

    async def create_post(
        self, data: PostCreateModelDomain, user: UserModelDomain
    ) -> HttpResponse: ...

    async def update_post(
        self, data: PostUpdatesModelDomain, user: UserModelDomain, post_id: int
    ) -> HttpResponse: ...

    async def get_post(self, post_id: int) -> HttpResponse: ...

    async def get_all_posts(self, filters: dict | None) -> HttpResponse: ...

    async def delete_post(
        self, post_id: int, user: UserModelDomain
    ) -> HttpResponse: ...

    async def execute(
        self,
        data: TSchema | None = None,
        user: UserModelDomain | None = None,
        post_id: int | None = None,
        method: Literal["POST", "GET", "PUT", "DELETE"] | None = None,
        filters: dict | None = None,
    ) -> HttpResponse:
        try:

            if data and isinstance(data, PostUpdatesModelDomain) and user and post_id:
                return await self.update_post(data=data, user=user, post_id=post_id)

            elif data and isinstance(data, PostCreateModelDomain) and user:
                return await self.create_post(data=data, user=user)

            elif post_id and user and method == "DELETE":
                return await self.delete_post(post_id=post_id, user=user)

            elif post_id and user and method == "GET":
                return await self.get_post(post_id=post_id)

            elif user and method == "GET":
                return await self.get_all_posts(filters=filters)

            return HttpResponse(
                status_code=501,
                body={"message": "Method not implemented"},
            )
        except Exception:
            return HttpResponse(
                status_code=501, body={"message": "Method not implemented"}
            )
