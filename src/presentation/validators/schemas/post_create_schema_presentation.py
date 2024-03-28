import re
from typing_extensions import Optional

from pydantic import Field, HttpUrl, field_validator
from src.domain.models.post_models_domain import PostCreateModelDomain


class PostCreateSchemaPresentation(PostCreateModelDomain):
    html: str = Field(..., min_length=50)
    images_urls: Optional[list[HttpUrl]] = Field(None)
    name: str = Field(..., min_length=5, max_length=255)

    @field_validator("html")
    def validate_descrption_is_html(cls, value: str):
        if re.match(r"<.*>", value) is None:
            raise ValueError("html must be html")
        return value
