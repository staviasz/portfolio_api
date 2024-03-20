from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func
from src.configs.repository.client_repository_config import Base
from sqlalchemy.orm import relationship


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    link_deploy = Column(Text, nullable=True)
    link_code = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    image = relationship("Image", back_populates="project")
    users = relationship(
        "User", secondary="user_project_association", back_populates="projects"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "link_deploy": self.link_deploy,
            "link_code": self.link_code,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "images_urls": [image.image_url for image in self.image],
        }
