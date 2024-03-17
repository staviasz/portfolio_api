from typing_extensions import Type, TypeVar
from sqlalchemy.orm import Session, DeclarativeBase
from src.presentation.types.orm_related_table_data_type_presentation import (
    OrmRelatedTable,
    OrmRelatedTableData,
)
from src.use_case.protocols.repository.repository_protocol_use_case import (
    RepositoryProtocolUseCase,
)

T = TypeVar("T", bound=DeclarativeBase)


class RepositoryInfra(RepositoryProtocolUseCase):
    def __init__(self, session: Session) -> None:
        self.session = session

    async def get_all(self, table_name: Type[T]) -> list[dict]:
        query_all = self.session.query(table_name).all()

        response = [row.__dict__ for row in query_all]
        return response

    async def get_by_email(self, table_name: type[T], email: str) -> dict | None:

        try:
            query = self.session.query(table_name).filter_by(email=email).first()
            if not query:
                return None

            return query.__dict__
        except Exception:
            return None

    async def get_by_id_instace(self, table_name: type[T], id: int) -> T:
        query = self.session.query(table_name).filter_by(id=id).first()

        if not query:
            raise ValueError("Id not found")

        return query

    async def get_by_id_dict(self, table_name: type[T], id: int) -> dict:
        query = self.session.query(table_name).filter_by(id=id).first()

        if not query:
            raise ValueError("Id not found")

        return query.__dict__

    async def create(
        self,
        table_name: type[T],
        data: dict,
    ) -> dict:

        query = table_name(**data)
        self.session.add(query)
        self.session.commit()
        self.session.refresh(query)
        del query.__dict__["_sa_instance_state"]
        return query.__dict__

    async def create_with_related(
        self,
        table_name: type[T],
        data: dict,
        related_table: list[OrmRelatedTableData],
    ) -> dict:

        query = table_name(**data)
        for related in related_table:
            data_list = []

            for related_data in related["data"]:
                data_list.append(related["table_name"](**related_data))

            setattr(query, related["field_in_principal_table"], data_list)

        self.session.add(query)
        self.session.commit()
        self.session.refresh(query)
        del query.__dict__["_sa_instance_state"]
        return query.__dict__

    async def update_with_related(
        self,
        table_name: Type[T],
        data: dict,
        related_table: list[OrmRelatedTableData],
        id: int,
    ) -> dict:
        query = await self.get_by_id_instace(table_name, id)

        for key, value in data.items():
            setattr(query, key, value)

        for related in related_table:
            related_instances = getattr(query, related["field_in_principal_table"])

            related_instances.clear()

            for related_data in related["data"]:
                related_instance = related["table_name"](**related_data)
                related_instances.append(related_instance)

        self.session.add(query)
        self.session.commit()
        self.session.refresh(query)
        del query.__dict__["_sa_instance_state"]

        return query.__dict__

    async def update(self, table_name: type[T], data: dict, id: int) -> dict:
        try:
            query = await self.get_by_id_instace(table_name, id)
            for key, value in data.items():
                if value:
                    setattr(query, key, value)

            self.session.commit()
            self.session.refresh(query)
            del query.__dict__["_sa_instance_state"]

            return query.__dict__
        except ValueError:
            raise ValueError("Id not found")

    async def delete(self, table_name: type[T], id: int) -> None:
        try:
            query = await self.get_by_id_instace(table_name, id)
            self.session.delete(query)
            self.session.commit()
        except ValueError:
            raise ValueError("Id not found")
        except Exception as e:
            print("teste", e)

    async def delete_with_related(
        self, table_name: type[T], id: int, related_table: list[OrmRelatedTable]
    ) -> None:
        query = await self.get_by_id_instace(table_name, id)

        for related in related_table:
            related_instances = getattr(query, related["table_name"].__tablename__)

            for related_instance in related_instances:
                self.session.delete(related_instance)

        self.session.delete(query)
        self.session.commit()
