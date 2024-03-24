from unittest.mock import Mock

from src.domain.models.user_models_domain import UserModelDomain
from src.use_case.implements.post.post_implements_use_case import PostUseCase
from src.use_case.protocols.repository.repository_protocol_use_case import (
    RepositoryProtocolUseCase,
)


repository = Mock(spec_set=RepositoryProtocolUseCase)
use_case = PostUseCase(repository=repository)

data = {"id": 1, "html": "<>post html</>"}
user = UserModelDomain(
    id=1,
    name="name",
    email="email",
    password="password",
    image_url="image_url",
    description="description",
    contact_description="contact_description",
)
