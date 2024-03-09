import pytest

from alembic import command
from src.infra.repository.run_migrations_repository_infra import alembic_config


def pytest_unconfigure(config):
    alembic_config
    command.downgrade(alembic_config, "base")


def pytest_collection_modifyitems(config, items):
    for item in items:
        if "db_setup" in item.keywords:
            item.add_marker(pytest.mark.db_setup)
