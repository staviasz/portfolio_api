from typing_extensions import Optional
from pydantic import Field, HttpUrl, root_validator
from src.domain.models.project_models_domain import ProjectModelUpdateDomain
from src.presentation.types.image_upload_type_presentation import ImageUpload


class ProjectUpdateSchema(ProjectModelUpdateDomain):
    name: Optional[str] = Field(None, min_length=5, max_length=150)
    description: Optional[str] = Field(None, min_length=50, max_length=1000)
    link_deploy: Optional[HttpUrl] = Field(None)
    link_code: Optional[HttpUrl] = Field(None)
    images_uploads: Optional[list[ImageUpload]] = Field(None)
    techs: Optional[list[int]] = Field(None)

    @root_validator(pre=True)
    def validate_all_fields_are_none(cls, values):
        if all(value is None for value in values.values()):
            raise ValueError("All fields are null.")
        return values
