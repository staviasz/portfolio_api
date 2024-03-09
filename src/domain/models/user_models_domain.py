from typing_extensions import Optional
from pydantic import BaseModel


class UserModelDomain(BaseModel):
    id: int
    name: str
    email: str
    password: str
    description: str
    contact_description: str
    image_url: str

    def model_dump(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "description": self.description,
            "contact_description": self.contact_description,
            "image_url": self.image_url,
        }


class ImageUpload(BaseModel):
    filename: str
    minetype: str
    body: bytes


class UserModelCreateDomain(BaseModel):
    name: str
    email: str
    password: str
    description: str
    contact_description: str
    image_upload: ImageUpload


class UserModelUpdateDomain(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    description: Optional[str]
    contact_description: Optional[str]
