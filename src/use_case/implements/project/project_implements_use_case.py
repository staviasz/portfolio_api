from src.domain.models.project_models_domain import (
    ProjectModelCreateDomain,
    ProjectModelDomain,
    ProjectModelUpdateDomain,
)
from src.domain.models.user_models_domain import UserModelDomain
from src.domain.protocols.project_protocols_domain import ProjectDomainProtocol
from src.infra.repository.models.Image_model_repository_infra import Image
from src.infra.repository.models.user_project_model_repository_infra import (
    UserProjectAssociation,
)
from src.infra.repository.models.project_model_repository_infra import Project
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.presentation.types.http_types_presentation import HttpResponse
from src.use_case.protocols.aws.aws_protocol_use_case import AwsProtocolUseCase
from src.use_case.protocols.repository.repository_protocol_use_case import (
    RepositoryProtocolUseCase,
)


class ProjectUseCase(ProjectDomainProtocol):
    def __init__(
        self, repository: RepositoryProtocolUseCase, bucket: AwsProtocolUseCase
    ):
        self.repository = repository
        self.bucket = bucket

    async def add_project(
        self, data: ProjectModelCreateDomain, user: UserModelDomain
    ) -> HttpResponse:
        try:
            images_urls = await self.bucket.upload(
                folder="projects", file=data.images_uploads
            )

            new_data = {**data.model_dump()}
            del new_data["images_uploads"]

            response = await self.repository.create_with_related(
                table_name=Project,
                data=new_data,
                related_table=[
                    {
                        "table_name": Image,
                        "field_in_principal_table": "image",
                        "data": [{"image_url": image_url} for image_url in images_urls],
                    },
                    {
                        "table_name": UserProjectAssociation,
                        "field_in_principal_table": "users",
                        "data": [{"user_id": user.id}],
                    },
                ],
            )

            project = ProjectModelDomain(**response)

            return HttpResponse(status_code=201, body=project.model_dump())
        except ExceptionCustomPresentation as error:
            return HttpResponse(status_code=error.status_code, body=error.body)

    async def edit_project(
        self, data: ProjectModelUpdateDomain, user: UserModelDomain, project_id: int
    ) -> HttpResponse:

        try:

            new_data = {**data.model_dump()}
            del new_data["images_uploads"]
            response = None
            if data.images_uploads:
                images_urls = []
                for image in data.images_uploads:
                    image_url = await self.bucket.upload(folder="projects", file=image)
                    images_urls.append(image_url)

                response = await self.repository.update_with_related(
                    table_name=Project,
                    data=new_data,
                    related_table=[
                        {
                            "table_name": Image,
                            "field_in_principal_table": "image",
                            "data": [{"image_url": image} for image in images_urls],
                        }
                    ],
                    id=project_id,
                )

            else:
                response = await self.repository.update(
                    table_name=Project,
                    data=new_data,
                    id=project_id,
                )

            project = ProjectModelDomain(**response)

            return HttpResponse(status_code=200, body=project.model_dump())
        except ExceptionCustomPresentation as error:
            return HttpResponse(status_code=error.status_code, body=error.body)

    async def get_project(self, project_id: int) -> HttpResponse:
        try:
            response = await self.repository.get_by_id_dict(
                table_name=Project, id=project_id
            )
            project = ProjectModelDomain(**response)

            return HttpResponse(status_code=200, body=project.model_dump())
        except ExceptionCustomPresentation as error:
            return HttpResponse(status_code=error.status_code, body=error.body)

    async def get_all_projects(self) -> HttpResponse:
        try:
            response = await self.repository.get_all(table_name=Project)
            projects = [
                ProjectModelDomain(**project).model_dump() for project in response
            ]
            return HttpResponse(status_code=200, body=projects)
        except ExceptionCustomPresentation as error:
            return HttpResponse(status_code=error.status_code, body=error.body)

    async def delete_project(self, project_id: int) -> HttpResponse:
        try:
            await self.repository.delete_with_related(
                id=project_id,
                table_name=Project,
                related_table=[
                    {"field_in_principal_table": "image", "table_name": Image}
                ],
            )
            return HttpResponse(status_code=204, body={})

        except ExceptionCustomPresentation as error:
            return HttpResponse(status_code=error.status_code, body=error.body)
