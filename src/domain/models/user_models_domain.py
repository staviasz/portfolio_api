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

    def model_all_dump(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "description": self.description,
            "contact_description": self.contact_description,
            "image_url": self.image_url,
        }

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
    mimetype: str
    body: bytes

    def model_dump(self):
        return {
            "filename": self.filename,
            "mimetype": self.mimetype,
            "body": self.body,
        }


class UserModelCreateDomain(BaseModel):
    name: str
    email: str
    password: str
    description: str
    contact_description: str
    image_upload: ImageUpload

    def model_dump(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "description": self.description,
            "contact_description": self.contact_description,
            "image_upload": self.image_upload.model_dump(),
        }


class UserModelUpdateDomain(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    description: Optional[str]
    contact_description: Optional[str]
    image_upload: Optional[ImageUpload]

    def model_dump(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "description": self.description,
            "contact_description": self.contact_description,
            "image_upload": (
                self.image_upload.model_dump() if self.image_upload else None
            ),
        }
