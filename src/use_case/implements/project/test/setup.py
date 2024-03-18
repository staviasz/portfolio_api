from unittest.mock import Mock


from src.domain.models.user_models_domain import UserModelDomain
from src.use_case.implements.project.project_implements_use_case import ProjectUseCase
from src.use_case.protocols.aws.aws_protocol_use_case import AwsProtocolUseCase
from src.use_case.protocols.repository.repository_protocol_use_case import (
    RepositoryProtocolUseCase,
)


repository = Mock(spec_set=RepositoryProtocolUseCase)
bucket = Mock(spec_set=AwsProtocolUseCase)

use_case = ProjectUseCase(repository=repository, bucket=bucket)

user = UserModelDomain(
    id=1,
    name="name",
    email="email",
    password="password",
    description="description",
    contact_description="contact_description",
    image_url="image_url",
)

data = {
    "description": "test",
    "images_uploads": [
        {
            "filename": "teste.txt",
            "body": b"teste",
            "mimetype": "text/plain",
        }
    ],
    "link_code": "https://github.com",
    "name": "test",
    "link_deploy": "https://github.com",
}
