from src.domain.models.post_models_domain import (
    PostDomain,
    PostCreateModelDomain,
    PostUpdatesModelDomain,
)
from src.domain.models.user_models_domain import UserModelDomain
from src.domain.protocols.post_protocols_domain import PostDomainProtocol
from src.infra.repository.models.Image_model_repository_infra import Image
from src.infra.repository.models.post_model_repository_infra import Post
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.presentation.types.http_types_presentation import HttpResponse
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
            del new_data["images_urls"]

            reponse = None
            if data.images_urls:
                reponse = await self.repository.create_with_related(
                    table_name=Post,
                    data=new_data,
                    related_table=[
                        {
                            "field_in_principal_table": "image",
                            "table_name": Image,
                            "data": [
                                {"image_url": str(image_url)}
                                for image_url in data.images_urls
                            ],
                            "field_forengein_key": "post_id",
                        }
                    ],
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
            post = await self.repository.get_by_id_dict(table_name=Post, id=post_id)

            if not post or post["user_id"] != user.id:
                return HttpResponse(status_code=404, body={"message": "Post not found"})

            reponse = await self.repository.update(
                table_name=Post, data=data.model_dump(), id=post_id
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
                await self.bucket.delete_upload(last_url_file=post["images_urls"])

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
