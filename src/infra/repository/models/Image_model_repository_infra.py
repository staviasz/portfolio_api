from sqlalchemy import (
    CheckConstraint,
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
    project_id = Column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=True
    )
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=True)

    project = relationship("Project", back_populates="image")
    posts = relationship("Post", back_populates="image")

    __table_args__ = (
        ForeignKeyConstraint(["project_id"], ["projects.id"], name="fk_project_id"),
        ForeignKeyConstraint(["post_id"], ["posts.id"], name="fk_post_id"),
        CheckConstraint(
            "(project_id IS NOT NULL OR post_id IS NOT NULL) AND (project_id IS NULL OR post_id IS NULL)"
        ),
    )
