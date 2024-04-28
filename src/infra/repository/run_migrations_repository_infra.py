from alembic.config import Config
from alembic import command


alembic_config = Config("alembic.ini")


def run_migrations() -> None:
    command.upgrade(alembic_config, "head")


if __name__ == "__main__":
    run_migrations()
