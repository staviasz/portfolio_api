from typing_extensions import Literal, Protocol, TypeVar

from pydantic import BaseModel

from src.domain.models.project_models_domain import (
    ProjectModelCreateDomain,
    ProjectModelUpdateDomain,
)
from src.domain.models.user_models_domain import UserModelDomain
from src.presentation.types.http_types_presentation import HttpResponse

TSchema = TypeVar("TSchema", bound=BaseModel)


class ProjectDomainProtocol(Protocol):

    async def add_project(
        self, data: ProjectModelCreateDomain, user: UserModelDomain
    ) -> HttpResponse: ...

    async def edit_project(
        self, data: ProjectModelUpdateDomain, user: UserModelDomain, project_id: int
    ) -> HttpResponse: ...

    async def get_project(self, project_id: int) -> HttpResponse: ...

    async def get_all_projects(self) -> HttpResponse: ...

    async def delete_project(self, project_id: int) -> HttpResponse: ...

    async def execute(
        self,
        data: TSchema | None = None,
        user: UserModelDomain | None = None,
        project_id: int | None = None,
        method: Literal["POST", "GET", "PUT", "DELETE"] | None = None,
    ) -> HttpResponse:

        if data and isinstance(data, ProjectModelCreateDomain) and user:
            return await self.add_project(data=data, user=user)

        elif (
            data and isinstance(data, ProjectModelUpdateDomain) and user and project_id
        ):
            return await self.edit_project(data=data, user=user, project_id=project_id)

        elif project_id and user:
            return await self.get_project(project_id=project_id)

        elif project_id and method == "DELETE":
            return await self.delete_project(project_id=project_id)

        elif project_id and method == "GET":
            return await self.get_project(project_id=project_id)

        elif not method:
            return await self.get_all_projects()

        return HttpResponse(
            status_code=500,
            body={"message": "Method not implemented"},
        )
