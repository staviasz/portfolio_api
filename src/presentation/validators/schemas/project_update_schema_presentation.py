from pydantic import Field, HttpUrl
from src.domain.models.project_models_domain import ProjectModelUpdateDomain
from src.presentation.types.image_upload_type_presentation import ImageUpload


class ProjectCreateSchema(ProjectModelUpdateDomain):
    name: str | None = Field(None, min_length=5, max_length=150)
    description: str | None = Field(None, min_length=50, max_length=1000)
    link_deploy: HttpUrl | None = Field(None)
    link_code: HttpUrl | None = Field(None)
    images_uploads: list[ImageUpload] | None = Field(None)
