import re

from pydantic import Field, field_validator
from src.domain.models.post_models_domain import PostModelDomain


class PostSchemaPresentation(PostModelDomain):
    html: str = Field(..., min_length=50)

    @field_validator("html")
    def validate_descrption_is_html(cls, value: str):
        if re.match(r"<.*>", value) is None:
            raise ValueError("html must be html")
        return value
