from unittest.mock import Mock
import pytest

from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)
from src.use_case.implements.tech.tech_implements_use_case import TechUsaCase
from src.use_case.protocols.repository.repository_protocol_use_case import (
    RepositoryProtocolUseCase,
)

repository = Mock(spec_set=RepositoryProtocolUseCase)
use_case = TechUsaCase(repository=repository)


@pytest.mark.asyncio
class TestTechImplementsUseCase:
    async def test_execute(self):
        repository.get_all.return_value = [
            {
                "id": 1,
                "name": "test",
                "created_at": "2022-01-01",
                "updated_at": "2022-01-01",
            }
        ]

        response = await use_case.execute()

        assert response.status_code == 200
        assert response.body == [{"id": 1, "name": "test"}]

    async def test_execute_exception(self):
        repository.get_all.side_effect = ExceptionCustomPresentation(
            status_code=500, type="Error Server", message="Error Execute Server"
        )

        response = await use_case.execute()

        assert response.status_code == 500
        assert response.body == {
            "type": "Error Server",
            "message": "Error Execute Server",
        }
