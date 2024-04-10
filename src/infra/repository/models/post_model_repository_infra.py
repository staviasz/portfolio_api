from sqlalchemy import Column, ForeignKey, ForeignKeyConstraint, Integer, String, Text
from src.configs.repository.client_repository_config import Base
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    html = Column(Text)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="posts")
    image = relationship(
        "Image",
        back_populates="posts",
        cascade="all, delete-orphan",
        single_parent=True,
    )

    techs = relationship(
        "Tech",
        secondary="post_tech_association",
        back_populates="posts",
        passive_deletes=True,
    )

    __table_args__ = (
        ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_user_id"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "html": self.html,
            "name": self.name,
            "user_id": self.user_id,
            "images_urls": [image.image_url for image in self.image if image],
            "techs": [tech.name for tech in self.techs if tech],
        }
