from typing_extensions import Type, TypeVar, Optional
from sqlalchemy.orm import Session, DeclarativeBase
from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
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

    async def get_all(
        self, table_name: Type[T], filters: Optional[dict] = None
    ) -> list[dict]:
        try:
            query = self.session.query(table_name)

            if filters:
                for key, value in filters.items():
                    query = query.filter(getattr(table_name, key) == value)

            query_all = query.all()

            response = [
                row.to_dict() if hasattr(row, "to_dict") else row.__dict__
                for row in query_all
            ]

            return response
        except Exception:
            raise ExceptionCustomPresentation(
                status_code=500,
                type="Server Error",
                message="Repository get all error",
            )

    async def get_by_email(self, table_name: type[T], email: str) -> dict | None:

        try:
            query = self.session.query(table_name).filter_by(email=email).first()
            if not query:
                return None

            return query.__dict__
        except Exception:
            raise ExceptionCustomPresentation(
                status_code=500,
                type="Server Error",
                message="Repository get by email error",
            )

    async def get_by_id_instace(self, table_name: type[T], id: int) -> T:
        try:
            query = self.session.query(table_name).filter_by(id=id).first()

            if not query:
                raise ValueError("Id not found")

            return query
        except Exception:
            raise ExceptionCustomPresentation(
                status_code=500,
                type="Server Error",
                message="Repository get by id error",
            )

    async def get_by_id_dict(self, table_name: type[T], id: int) -> dict:

        try:
            query = self.session.query(table_name).filter_by(id=id).first()

            if not query:
                raise ValueError("Id not found")
            if hasattr(query, "to_dict"):
                return query.to_dict()
            return query.__dict__
        except Exception:
            raise ExceptionCustomPresentation(
                status_code=500,
                type="Server Error",
                message="Repository get by id error",
            )

    async def create(
        self,
        table_name: type[T],
        data: dict,
    ) -> dict:
        try:
            query = table_name(**data)
            self.session.add(query)
            self.session.commit()
            self.session.refresh(query)
            del query.__dict__["_sa_instance_state"]
            return query.__dict__

        except Exception:
            raise ExceptionCustomPresentation(
                status_code=500,
                type="Server Error",
                message="Repository create error",
            )

    async def create_with_related(
        self,
        table_name: type[T],
        data: dict,
        related_table: list[OrmRelatedTableData],
    ) -> dict:
        try:
            entity = table_name(**data)
            self.session.add(entity)
            self.session.flush()
            project_id = entity.__dict__["id"]

            for related_data in related_table:
                field_in_principal_table = related_data["field_in_principal_table"]
                related_table_class = related_data["table_name"]
                related_data_to_insert = related_data["data"]
                for related_data_item in related_data_to_insert:
                    new_data = {**related_data_item, "project_id": project_id}
                    related_entity = related_table_class(**new_data)
                    setattr(related_entity, field_in_principal_table, entity)
                    self.session.add(related_entity)

            self.session.commit()
            self.session.refresh(entity)
            if hasattr(entity, "to_dict"):
                return entity.to_dict()
            return entity.__dict__

        except Exception:
            raise ExceptionCustomPresentation(
                status_code=500,
                type="Server Error",
                message="Repository create error",
            )

    async def update_with_related(
        self,
        table_name: Type[T],
        data: dict,
        related_table: list[OrmRelatedTableData],
        id: int,
    ) -> dict:
        try:
            query = await self.get_by_id_instace(table_name, id)

            for key, value in data.items():
                if value and value != "None":
                    setattr(query, key, value)

            for related in related_table:
                self.session.query(related["table_name"]).filter_by(
                    project_id=id
                ).delete()
                self.session.commit()
                related_instances = getattr(query, related["field_in_principal_table"])

                for related_data_item in related["data"]:
                    new_data = {**related_data_item, "project_id": id}
                    related_instance = related["table_name"](**new_data)
                    related_instances.append(related_instance)

            self.session.add(query)
            self.session.commit()
            self.session.refresh(query)

            if hasattr(query, "to_dict"):
                return query.to_dict()

            del query.__dict__["_sa_instance_state"]
            return query.__dict__
        except Exception:
            raise ExceptionCustomPresentation(
                status_code=500,
                type="Server Error",
                message="Repository update error",
            )

    async def update(self, table_name: type[T], data: dict, id: int) -> dict:
        try:
            query = await self.get_by_id_instace(table_name, id)
            for key, value in data.items():
                if value and value != "None":
                    setattr(query, key, value)

            self.session.commit()
            self.session.refresh(query)

            if hasattr(query, "to_dict"):
                return query.to_dict()

            del query.__dict__["_sa_instance_state"]
            return query.__dict__
        except Exception:
            raise ExceptionCustomPresentation(
                status_code=500,
                type="Server Error",
                message="Repository update error",
            )

    async def delete(self, table_name: type[T], id: int) -> None:
        try:
            query = await self.get_by_id_instace(table_name, id)
            self.session.delete(query)
            self.session.commit()
        except Exception:
            raise ExceptionCustomPresentation(
                status_code=500,
                type="Server Error",
                message="Repository delete error",
            )

    async def delete_with_related(
        self, table_name: type[T], id: int, related_table: list[OrmRelatedTable]
    ) -> None:
        try:
            query = await self.get_by_id_instace(table_name, id)

            for related in related_table:
                related_instances = getattr(query, related["table_name"].__tablename__)

                for related_instance in related_instances:
                    self.session.delete(related_instance)

            self.session.delete(query)
            self.session.commit()

        except Exception:
            raise ExceptionCustomPresentation(
                status_code=500,
                type="Server Error",
                message="Repository delete error",
            )
