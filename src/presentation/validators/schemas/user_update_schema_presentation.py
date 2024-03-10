import re
from typing_extensions import Optional
from pydantic import Field, EmailStr, field_validator
from src.domain.models.user_models_domain import ImageUpload, UserModelUpdateDomain


class UserUpdateSchema(UserModelUpdateDomain):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    email: Optional[EmailStr] = Field(None, min_length=3, max_length=150)
    password: Optional[str] = Field(None, min_length=8, max_length=20)
    description: Optional[str] = Field(None, min_length=50)
    contact_description: Optional[str] = Field(None, min_length=50)
    image_upload: Optional[ImageUpload]

    @field_validator("name")
    def validate_name(cls, value: str):
        if value and re.match(r"^[a-zA-ZÀ-ÿ]+$", value) is None:
            raise ValueError("Name must be only letters")
        return value

    def validate_descrption_is_html(cls, value: str):
        if value and re.match(r"<.*>", value) is None:
            raise ValueError("Description must be html")
        return value

    def validate_password(cls, value: str):
        if value and (
            re.match(
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
                value,
            )
            is None
        ):
            raise ValueError(
                """Password must contain at least one lowercase letter, one uppercase letter,
                one digit, one special character, and be at least 8 characters long"""
            )
        return value
