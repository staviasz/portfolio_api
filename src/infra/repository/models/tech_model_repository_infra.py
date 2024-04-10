from sqlalchemy import Column, Integer, String, DateTime
from src.configs.repository.client_repository_config import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Tech(Base):
    __tablename__ = "techs"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    users = relationship(
        "User", secondary="user_tech_association", back_populates="techs"
    )
    projects = relationship(
        "Project", secondary="project_tech_association", back_populates="techs"
    )
    posts = relationship(
        "Post", secondary="post_tech_association", back_populates="techs"
    )
