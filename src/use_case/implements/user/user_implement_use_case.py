import asyncio
from src.domain.models.user_models_domain import (
    UserModelCreateDomain,
    UserModelDomain,
    UserModelUpdateDomain,
)
from src.domain.protocols.user_protocols_domain import UserDomainProtocol
from src.infra.repository.models.tech_model_repository_infra import Tech
from src.infra.repository.models.user_model_repository_infra import User
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.presentation.types.http_types_presentation import HttpResponse
from src.use_case.protocols.aws.aws_protocol_use_case import AwsProtocolUseCase
from src.use_case.protocols.bycript.bycript_protocol_use_case import (
    BycryptProtocolUseCase,
)
from src.use_case.protocols.repository.repository_protocol_use_case import (
    RepositoryProtocolUseCase,
)
from src.infra.repository.models.user_tech_model_repository_infra import (
    UsertechAssociation,
)


class UserUseCase(UserDomainProtocol):

    def __init__(
        self,
        repository: RepositoryProtocolUseCase,
        bucket: AwsProtocolUseCase,
        hasher: BycryptProtocolUseCase,
    ) -> None:
        self.repository = repository
        self.bucket = bucket
        self.hasher = hasher

    async def add_user(self, user: UserModelCreateDomain) -> HttpResponse:
        try:
            data = {**user.model_dump()}
            data["password"] = await self.hasher.hash(user.password)
            del data["image_upload"]

            if await self.repository.get_by_email(User, user.email):
                return HttpResponse(
                    status_code=409, body={"message": "Email already exists"}
                )

            data["image_url"] = await self.bucket.upload(
                file=user.image_upload, folder="users"
            )

            new_user = None
            if user.techs:
                del data["techs"]
                exists_techs = [
                    self.repository.get_by_id_dict(table_name=Tech, id=tech_id)
                    for tech_id in user.techs
                ]
                await asyncio.gather(*exists_techs)
                new_user = await self.repository.create_with_related(
                    table_name=User,
                    data=data,
                    related_table=[
                        {
                            "table_name": UsertechAssociation,
                            "field_in_principal_table": "users",
                            "data": [{"tech_id": tech} for tech in user.techs],
                            "field_forengein_key": "user_id",
                        },
                    ],
                )
            else:
                new_user = await self.repository.create(table_name=User, data=data)

            response: UserModelDomain = UserModelDomain(**new_user)

            return HttpResponse(status_code=201, body=response.model_dump())
        except ExceptionCustomPresentation as error:
            return HttpResponse(status_code=error.status_code, body=error.body)

    async def edit_user(
        self, user: dict, data_user: UserModelUpdateDomain
    ) -> HttpResponse:
        try:

            data = {**data_user.model_dump()}

            if data_user.password:
                data["password"] = await self.hasher.hash(data_user.password)
            if data_user.email:
                user_current = await self.repository.get_by_email(User, data_user.email)
                if user_current and user_current["id"] != user["id"]:
                    return HttpResponse(
                        status_code=409, body={"message": "Email already exists"}
                    )

            if data_user.image_upload:
                del data["image_upload"]
                data["image_url"] = await self.bucket.update_upload(
                    last_url_file=user["image_url"],
                    file=data_user.image_upload,
                    folder="users",
                )

            update_user = None
            if data_user.techs:
                del data["techs"]

                exists_techs = [
                    self.repository.get_by_id_dict(table_name=Tech, id=tech_id)
                    for tech_id in data_user.techs
                ]
                await asyncio.gather(*exists_techs)

                update_user = await self.repository.update_with_related(
                    table_name=User,
                    data=data,
                    related_table=[
                        {
                            "table_name": UsertechAssociation,
                            "field_in_principal_table": "techs",
                            "data": [{"tech_id": tech} for tech in data_user.techs],
                            "field_forengein_key": "user_id",
                        },
                    ],
                    id=user["id"],
                )
            else:
                update_user = await self.repository.update(
                    table_name=User, data=data, id=user["id"]
                )
            response: UserModelDomain = UserModelDomain(**update_user)

            return HttpResponse(status_code=200, body=response.model_dump())

        except ExceptionCustomPresentation as error:
            return HttpResponse(status_code=error.status_code, body=error.body)

    async def get_all_users(self) -> HttpResponse:
        try:
            users = await self.repository.get_all(table_name=User)

            response = [UserModelDomain(**user).model_dump() for user in users]

            return HttpResponse(status_code=200, body=response)

        except ExceptionCustomPresentation as error:
            return HttpResponse(status_code=error.status_code, body=error.body)

    async def get_user(self, user_id: int) -> HttpResponse:
        try:
            user = await self.repository.get_by_id_dict(table_name=User, id=user_id)
            print(user)
            response = UserModelDomain(**user)

            return HttpResponse(status_code=200, body=response.model_dump())

        except ExceptionCustomPresentation as error:
            return HttpResponse(status_code=error.status_code, body=error.body)

    async def delete_user(self, user_id: int) -> HttpResponse:
        try:
            user = await self.repository.delete(table_name=User, id=user_id)
            await self.bucket.delete_upload(last_url_file=user["image_url"])

            return HttpResponse(status_code=204, body={})

        except ExceptionCustomPresentation as error:
            return HttpResponse(status_code=error.status_code, body=error.body)
