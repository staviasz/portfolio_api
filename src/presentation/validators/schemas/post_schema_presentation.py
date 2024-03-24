import re

from pydantic import Field, field_validator
from src.domain.models.post_models_domain import PostModelCreateDomain


class PostSchemaPresentation(PostModelCreateDomain):
    html: str = Field(..., min_length=50)

    @field_validator("html")
    def validate_descrption_is_html(cls, value: str):
        if re.match(r"<.*>", value) is None:
            raise ValueError("Description must be html")
        return value
