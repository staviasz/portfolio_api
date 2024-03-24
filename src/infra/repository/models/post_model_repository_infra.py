from sqlalchemy import Column, ForeignKey, ForeignKeyConstraint, Integer, Text
from src.configs.repository.client_repository_config import Base
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    html = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="posts")

    __table_args__ = (
        ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_user_id"),
    )
