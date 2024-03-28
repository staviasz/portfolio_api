import re
from typing_extensions import Optional

from pydantic import Field, HttpUrl, field_validator, root_validator
from src.domain.models.post_models_domain import PostUpdatesModelDomain


class PostUpdateSchemaPresentation(PostUpdatesModelDomain):
    html: Optional[str] = Field(None, min_length=50)
    images_urls: Optional[list[HttpUrl]] = Field(None)
    name: Optional[str] = Field(None, min_length=5, max_length=255)

    @root_validator(pre=True)
    def validate_all_fields_are_none(cls, values):
        if all(value is None for value in values.values()):
            raise ValueError("All fields are null.")
        return values

    @field_validator("html")
    def validate_descrption_is_html(cls, value: str):
        if re.match(r"<.*>", value) is None:
            raise ValueError("html must be html")
        return value
