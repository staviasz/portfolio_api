import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.configs.pydantic.pydantic_env_settings_config import PydanticEnv

current_dir = os.path.dirname(__file__)
sqlite_db_file = os.path.abspath(os.path.join(current_dir, "../../../sqlite.db"))

env = PydanticEnv().env

engine = None
if env == "dev":
    engine = create_engine(url=PydanticEnv().database_url, pool_size=50)
elif env == "test":
    engine = create_engine(
        f"sqlite:///{sqlite_db_file}", connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
