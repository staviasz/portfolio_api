import asyncio

from pydantic import HttpUrl
from src.configs.pydantic.pydantic_env_settings_config import PydanticEnv
from src.domain.models.post_models_domain import (
    PostDomain,
    PostCreateModelDomain,
    PostUpdatesModelDomain,
)
from src.domain.models.user_models_domain import UserModelDomain
from src.domain.protocols.post_protocols_domain import PostDomainProtocol
from src.infra.repository.models.Image_model_repository_infra import Image
from src.infra.repository.models.post_model_repository_infra import Post
from src.infra.repository.models.post_tech_model_repository_infra import (
    PostTechAssociation,
)
from src.infra.repository.models.tech_model_repository_infra import Tech
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


class PostUseCase(PostDomainProtocol):
    def __init__(
        self, repository: RepositoryProtocolUseCase, bucket: AwsProtocolUseCase
    ) -> None:
        self.repository = repository
        self.bucket = bucket

    async def create_post(
        self, data: PostCreateModelDomain, user: UserModelDomain
    ) -> HttpResponse:
        try:
            new_data = {**data.model_dump(), "user_id": user.id}

            reponse = None
            related_table_data = await self.__related_table_data(
                data.images_urls, data.techs
            )

            if related_table_data:
                if data.images_urls:
                    del new_data["images_urls"]
                if data.techs:
                    del new_data["techs"]

                reponse = await self.repository.create_with_related(
                    table_name=Post, data=new_data, related_table=related_table_data
                )

            else:
                reponse = await self.repository.create(table_name=Post, data=new_data)

            result = PostDomain(**reponse).model_dump()

            return HttpResponse(status_code=201, body=result)

        except ExceptionCustomPresentation as error:
            return HttpResponse(status_code=error.status_code, body=error.body)

    async def update_post(
        self, data: PostUpdatesModelDomain, user: UserModelDomain, post_id: int
    ) -> HttpResponse:
        try:
            new_data = {**data.model_dump()}
            print(new_data)
            post = await self.repository.get_by_id_dict(table_name=Post, id=post_id)

            if not post or post["user_id"] != user.id:
                return HttpResponse(status_code=404, body={"message": "Post not found"})

            reponse = None
            related_table_data = await self.__related_table_data(
                data.images_urls, data.techs
            )

            if related_table_data:
                if data.images_urls:
                    del new_data["images_urls"]
                if data.techs:
                    del new_data["techs"]

                reponse = await self.repository.update_with_related(
                    table_name=Post,
                    data=new_data,
                    related_table=related_table_data,
                    id=post_id,
                )

            else:
                reponse = await self.repository.update(
                    table_name=Post, data=new_data, id=post_id
                )

            result = PostDomain(**reponse).model_dump()

            return HttpResponse(status_code=200, body=result)

        except ExceptionCustomPresentation as error:
            return HttpResponse(status_code=error.status_code, body=error.body)

    async def get_post(self, post_id: int) -> HttpResponse:
        try:
            post = await self.repository.get_by_id_dict(table_name=Post, id=post_id)

            if not post:
                return HttpResponse(status_code=404, body={"message": "Post not found"})

            result = PostDomain(**post).model_dump()

            return HttpResponse(status_code=200, body=result)

        except ExceptionCustomPresentation as error:
            return HttpResponse(status_code=error.status_code, body=error.body)

    async def delete_post(self, post_id: int, user: UserModelDomain) -> HttpResponse:
        try:
            post = await self.repository.get_by_id_dict(table_name=Post, id=post_id)

            if not post or post["user_id"] != user.id:
                return HttpResponse(status_code=404, body={"message": "Post not found"})

            await self.repository.delete(table_name=Post, id=post_id)

            if post["images_urls"]:
                bucket_url = f"https://{PydanticEnv().bucket_endpoint}/{PydanticEnv().bucket_name}/"
                verify_url_bucket: list[str] = [
                    image_url
                    for image_url in post["images_urls"]
                    if bucket_url in image_url
                ]
                if verify_url_bucket:
                    await self.bucket.delete_upload(last_url_file=verify_url_bucket)

            return HttpResponse(status_code=204, body={})

        except ExceptionCustomPresentation as error:
            return HttpResponse(status_code=error.status_code, body=error.body)

    async def get_all_posts(self, filters: dict | None) -> HttpResponse:
        try:
            posts = await self.repository.get_all(table_name=Post, filters=filters)

            response = [PostDomain(**post).model_dump() for post in posts]

            return HttpResponse(status_code=200, body=response)

        except ExceptionCustomPresentation as error:
            return HttpResponse(status_code=error.status_code, body=error.body)

    async def __related_table_data(
        self,
        images_urls: list[HttpUrl] | None,
        techs: list[int] | None,
    ) -> list[OrmRelatedTableData] | None:
        try:
            related_table_data: list[OrmRelatedTableData] = []
            if images_urls:
                related_table_data.append(
                    {
                        "field_in_principal_table": "image",
                        "table_name": Image,
                        "data": [
                            {"image_url": str(image_url)} for image_url in images_urls
                        ],
                        "field_forengein_key": "post_id",
                    }
                )
            if techs:
                exists_techs = [
                    self.repository.get_by_id_dict(table_name=Tech, id=tech_id)
                    for tech_id in techs
                ]
                await asyncio.gather(*exists_techs)

                related_table_data.append(
                    {
                        "field_in_principal_table": "techs",
                        "table_name": PostTechAssociation,
                        "data": [{"tech_id": tech_id} for tech_id in techs],
                        "field_forengein_key": "post_id",
                    }
                )
            return related_table_data
        except ExceptionCustomPresentation as error:
            raise error
