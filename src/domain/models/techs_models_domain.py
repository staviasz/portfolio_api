from pydantic import BaseModel


class TechsModelsDomain(BaseModel):
    id: int
    name: str

    def model_dump(self):
        return {"id": self.id, "name": self.name}
