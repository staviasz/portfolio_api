from sqlalchemy import Column, DateTime, ForeignKey, Integer
from src.configs.repository.client_repository_config import Base
from sqlalchemy.sql import func


class UserProjectAssociation(Base):
    __tablename__ = "user_project_association"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), primary_key=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
