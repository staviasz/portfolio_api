from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.configs.repository.client_repository_config import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100))
    email = Column(String, unique=True)
    password = Column(String)
    description = Column(Text)
    contact_description = Column(Text)
    image_url = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    projects = relationship(
        "Project",
        secondary="user_project_association",
        back_populates="users",
        cascade="all, delete-orphan",
        single_parent=True,
    )
    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")
    techs = relationship(
        "Tech",
        secondary="user_tech_association",
        back_populates="users",
        passive_deletes=True,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "description": self.description,
            "contact_description": self.contact_description,
            "image_url": self.image_url,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "techs": [tech.name for tech in self.techs if tech],
        }
