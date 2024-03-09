from typing_extensions import Protocol, TypeVar, Type
from sqlalchemy.orm import DeclarativeBase

T = TypeVar("T", bound="DeclarativeBase")


class GetByEmailRepositoryProtocolUseCase(Protocol):

    async def get_by_email(self, table_name: Type[T], email: str) -> dict: ...
