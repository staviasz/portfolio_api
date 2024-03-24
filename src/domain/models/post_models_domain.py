from typing_extensions import Optional
from pydantic import BaseModel


class PostDomain(BaseModel):
    id: int
    html: str
    user_id: int

    def model_dump(self):
        return {
            "id": self.id,
            "html": self.html,
            "user_id": self.user_id,
        }


class PostModelCreateDomain(BaseModel):
    html: str


class PostModelUpdateDomain(BaseModel):
    id: int
    html: Optional[str]
