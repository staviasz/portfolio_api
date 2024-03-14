import re
from pydantic import EmailStr, Field, field_validator
from src.domain.models.login_models_domain import LoginModelDomain


class LoginSchemaPresentation(LoginModelDomain):
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8, max_length=20)

    @field_validator("password")
    def validate_password(cls, value: str):
        if (
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
