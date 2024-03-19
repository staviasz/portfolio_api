from sqlalchemy import (
    Column,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    Text,
)
from src.configs.repository.client_repository_config import Base
from sqlalchemy.orm import relationship


class Image(Base):
    __tablename__ = "image"

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(Text, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    project = relationship("Project", back_populates="image")

    __table_args__ = (
        ForeignKeyConstraint(["project_id"], ["projects.id"], name="fk_project_id"),
    )
