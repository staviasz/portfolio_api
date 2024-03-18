from pydantic import Field, HttpUrl
from src.domain.models.project_models_domain import ProjectModelCreateDomain
from src.presentation.types.image_upload_type_presentation import ImageUpload


class ProjectCreateSchema(ProjectModelCreateDomain):
    name: str = Field(..., min_length=5, max_length=150)
    description: str = Field(..., min_length=50, max_length=1000)
    link_deploy: HttpUrl = Field(...)
    link_code: HttpUrl = Field(...)
    images_uploads: list[ImageUpload] = Field(...)
