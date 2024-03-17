from sqlalchemy import Column, Integer, Text
from src.configs.repository.client_repository_config import Base


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    html = Column(Text)
