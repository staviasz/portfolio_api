import asyncio
from src.domain.models.project_models_domain import (
    ProjectModelCreateDomain,
    ProjectModelDomain,
    ProjectModelUpdateDomain,
)
from src.domain.models.user_models_domain import UserModelDomain
from src.domain.protocols.project_protocols_domain import ProjectDomainProtocol
from src.infra.repository.models.Image_model_repository_infra import Image
from src.infra.repository.models.project_tech_model_repository_infra import (
    ProjecttechAssociation,
)
from src.infra.repository.models.tech_model_repository_infra import Tech
from src.infra.repository.models.user_project_model_repository_infra import (
    UserProjectAssociation,
)
from src.infra.repository.models.project_model_repository_infra import Project
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.presentation.types.http_types_presentation import HttpResponse
from src.presentation.types.orm_related_table_data_type_presentation import (
    OrmRelatedTableData,
)
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

            related_table_data: list[OrmRelatedTableData] = [
                {
                    "table_name": Image,
                    "field_in_principal_table": "image",
                    "data": [{"image_url": image_url} for image_url in images_urls],
                    "field_forengein_key": "project_id",
                },
                {
                    "table_name": UserProjectAssociation,
                    "field_in_principal_table": "users",
                    "data": [{"user_id": user.id}],
                    "field_forengein_key": "project_id",
                },
            ]

            if data.techs:
                del new_data["techs"]
                exists_techs = [
                    self.repository.get_by_id_dict(table_name=Tech, id=tech_id)
                    for tech_id in data.techs
                ]
                await asyncio.gather(*exists_techs)

                related_table_data.append(
                    {
                        "table_name": ProjecttechAssociation,
                        "field_in_principal_table": "techs",
                        "data": [{"tech_id": tech_id} for tech_id in data.techs],
                        "field_forengein_key": "project_id",
                    }
                )

            response = await self.repository.create_with_related(
                table_name=Project, data=new_data, related_table=related_table_data
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

            response = None
            related_table_data: list[OrmRelatedTableData] = []

            if data.images_uploads:
                del new_data["images_uploads"]

                images_urls = [
                    await self.bucket.upload(folder="projects", file=image)
                    for image in data.images_uploads
                ]

                related_table_data.append(
                    {
                        "table_name": Image,
                        "field_in_principal_table": "image",
                        "data": [{"image_url": image_url} for image_url in images_urls],
                        "field_forengein_key": "project_id",
                    }
                )

            if data.techs:
                del new_data["techs"]
                exists_techs = [
                    self.repository.get_by_id_dict(table_name=Tech, id=tech_id)
                    for tech_id in data.techs
                ]
                await asyncio.gather(*exists_techs)

                related_table_data.append(
                    {
                        "table_name": ProjecttechAssociation,
                        "field_in_principal_table": "techs",
                        "data": [{"tech_id": tech_id} for tech_id in data.techs],
                        "field_forengein_key": "project_id",
                    }
                )

            if related_table_data:
                response = await self.repository.update_with_related(
                    table_name=Project,
                    data=new_data,
                    id=project_id,
                    related_table=related_table_data,
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
            project = await self.repository.delete(table_name=Project, id=project_id)
            await self.bucket.delete_upload(last_url_file=project["images_urls"])
            return HttpResponse(status_code=204, body={})

        except ExceptionCustomPresentation as error:
            return HttpResponse(status_code=error.status_code, body=error.body)
