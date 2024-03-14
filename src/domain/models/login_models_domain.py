from pydantic import BaseModel


class LoginModelDomain(BaseModel):
    email: str
    password: str
