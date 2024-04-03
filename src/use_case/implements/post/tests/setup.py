from unittest.mock import Mock

from src.domain.models.user_models_domain import UserModelDomain
from src.use_case.implements.post.post_implements_use_case import PostUseCase
from src.use_case.protocols.aws.aws_protocol_use_case import AwsProtocolUseCase
from src.use_case.protocols.repository.repository_protocol_use_case import (
    RepositoryProtocolUseCase,
)

bucket = Mock(spec_set=AwsProtocolUseCase)
repository = Mock(spec_set=RepositoryProtocolUseCase)
use_case = PostUseCase(repository=repository, bucket=bucket)

data = {
    "id": 1,
    "name": "name Post",
    "html": "<>post html</>",
    "images_urls": ["http://url1/", "http://url2/"],
}
user = UserModelDomain(
    id=1,
    name="name",
    email="email",
    password="password",
    image_url="image_url",
    description="description",
    contact_description="contact_description",
)
