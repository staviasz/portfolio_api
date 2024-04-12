from src.configs.repository.client_repository_config import SessionLocal
from src.infra.repository.implement.repository_infra import RepositoryInfra
from src.presentation.contracts.controller_contract_presentation import Controller
from src.presentation.controllers.tech.tech_controller_presentation import (
    TechController,
)
from src.use_case.implements.tech.tech_implements_use_case import TechUsaCase


def make_tech_factory() -> Controller:
    repository = RepositoryInfra(SessionLocal())
    use_case = TechUsaCase(repository=repository)
    return TechController(use_case=use_case)
