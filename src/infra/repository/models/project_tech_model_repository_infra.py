from sqlalchemy import Column, DateTime, ForeignKey, Integer
from src.configs.repository.client_repository_config import Base
from sqlalchemy.sql import func


class ProjecttechAssociation(Base):
    __tablename__ = "project_tech_association"
    project_id = Column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True
    )
    tech_id = Column(Integer, ForeignKey("techs.id"), primary_key=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
