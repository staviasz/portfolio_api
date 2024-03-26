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


class PostModelDomain(BaseModel):
    html: str

    def model_dump(self):
        return {
            "html": self.html,
        }
