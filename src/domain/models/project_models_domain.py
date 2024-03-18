from typing import Optional
from pydantic import BaseModel, HttpUrl

from src.presentation.types.image_upload_type_presentation import ImageUpload


class ProjectModelDomain(BaseModel):
    id: int
    name: str
    description: str
    link_deploy: str
    link_code: str
    images_urls: list[str]

    def model_dump(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "link_deploy": self.link_deploy,
            "link_code": self.link_code,
            "images_urls": self.images_urls,
        }


class ProjectModelCreateDomain(BaseModel):
    name: str
    description: str
    link_deploy: HttpUrl
    link_code: HttpUrl
    images_uploads: list[ImageUpload]

    def model_dump(self):
        return {
            "name": self.name,
            "description": self.description,
            "link_deploy": str(self.link_deploy),
            "link_code": str(self.link_code),
            "images_uploads": self.images_uploads,
        }


class ProjectModelUpdateDomain(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    link_deploy: Optional[HttpUrl] = None
    link_code: Optional[HttpUrl] = None
    images_uploads: Optional[list[ImageUpload]] = None

    def model_dump(self):
        list_images_dump = None
        if self.images_uploads:
            list_images_dump = []
            for image in self.images_uploads:
                list_images_dump.append(image.model_dump())

        return {
            "name": self.name,
            "description": self.description,
            "link_deploy": str(self.link_deploy),
            "link_code": str(self.link_code),
            "images_uploads": list_images_dump,
        }
