from src.domain.models.user_models_domain import (
    UserModelCreateDomain,
    UserModelDomain,
    UserModelUpdateDomain,
)
from src.domain.protocols.user_protocols_domain import UserDomainProtocol
from src.infra.repository.models.user_model_repository_infra import User
from src.presentation.types.http_types_presentation import HttpResponse
from src.use_case.protocols.aws.aws_protocol_use_case import AwsProtocolUseCase
from src.use_case.protocols.bycript.bycript_protocol_use_case import (
    BycryptProtocolUseCase,
)
from src.use_case.protocols.repository.repository_protocol_use_case import (
    RepositoryProtocolUseCase,
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

            new_user = await self.repository.create(table_name=User, data=data)

            response: UserModelDomain = UserModelDomain(**new_user)

            return HttpResponse(status_code=201, body=response.model_dump())
        except Exception as e:
            return HttpResponse(status_code=500, body={"Error": e})

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
                data["image_url"] = await self.bucket.update_upload(
                    last_url_file=user["image_url"],
                    file=data_user.image_upload,
                    folder="users",
                )

            update_user = await self.repository.update(
                table_name=User, data=data, id=user["id"]
            )
            print("data")

            response: UserModelDomain = UserModelDomain(**update_user)

            return HttpResponse(status_code=200, body=response.model_dump())

        except Exception as e:
            return HttpResponse(status_code=500, body={"Error": e})

    async def get_all_users(self) -> HttpResponse:
        try:
            users = await self.repository.get_all(table_name=User)

            response = [UserModelDomain(**user).model_dump() for user in users]

            return HttpResponse(status_code=200, body=response)

        except Exception as e:
            return HttpResponse(status_code=500, body={"Error": e})

    async def get_user(self, user: dict) -> HttpResponse:
        try:
            response = UserModelDomain(**user)

            return HttpResponse(status_code=200, body=response.model_dump())

        except Exception as e:
            return HttpResponse(status_code=500, body={"Error": e})

    async def delete_user(self, user_id: int) -> HttpResponse:
        try:
            await self.repository.delete(table_name=User, id=user_id)

            return HttpResponse(status_code=204, body={})

        except Exception as e:
            return HttpResponse(status_code=500, body={"Error": e})
