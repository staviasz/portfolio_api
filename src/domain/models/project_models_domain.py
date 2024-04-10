from typing import Optional
from pydantic import BaseModel, HttpUrl

from src.presentation.types.image_upload_type_presentation import ImageUpload
from src.utils.clean_data_dict import clean_dict_return


class ProjectModelDomain(BaseModel):
    id: int
    name: str
    description: str
    link_deploy: str
    link_code: str
    images_urls: list[str]
    techs: Optional[list[str]] = None

    def model_dump(self):
        return clean_dict_return(
            {
                "id": self.id,
                "name": self.name,
                "description": self.description,
                "link_deploy": self.link_deploy,
                "link_code": self.link_code,
                "images_urls": self.images_urls,
                "techs": self.techs,
            }
        )


class ProjectModelCreateDomain(BaseModel):
    name: str
    description: str
    link_deploy: Optional[HttpUrl] = None
    link_code: HttpUrl
    images_uploads: list[ImageUpload]
    techs: Optional[list[int]] = None

    def model_dump(self):
        return clean_dict_return(
            {
                "name": self.name,
                "description": self.description,
                "link_deploy": str(self.link_deploy),
                "link_code": str(self.link_code),
                "images_uploads": self.images_uploads,
                "techs": self.techs,
            }
        )


class ProjectModelUpdateDomain(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    link_deploy: Optional[HttpUrl] = None
    link_code: Optional[HttpUrl] = None
    images_uploads: Optional[list[ImageUpload]] = None
    techs: Optional[list[int]] = None

    def model_dump(self):
        return clean_dict_return(
            {
                "name": self.name,
                "description": self.description,
                "link_deploy": str(self.link_deploy),
                "link_code": str(self.link_code),
                "images_uploads": (
                    [image.model_dump() for image in self.images_uploads]
                    if self.images_uploads
                    else None
                ),
                "techs": self.techs,
            }
        )
