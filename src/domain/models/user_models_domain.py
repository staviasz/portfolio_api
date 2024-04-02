from typing_extensions import Optional
from pydantic import BaseModel

from src.presentation.types.image_upload_type_presentation import ImageUpload
from src.utils.clean_data_dict import clean_dict_return


class UserModelDomain(BaseModel):
    id: int
    name: str
    email: str
    password: str
    description: str
    contact_description: str
    image_url: str
    techs: Optional[list[str]] = None

    def model_all_dump(self) -> dict:
        return self.__clean_dict_return()

    def model_dump(self):
        data = self.__clean_dict_return()
        del data["password"]
        return data

    def __clean_dict_return(self):
        return clean_dict_return(
            {
                "id": self.id,
                "name": self.name,
                "email": self.email,
                "password": self.password,
                "description": self.description,
                "contact_description": self.contact_description,
                "image_url": self.image_url,
                "techs": self.techs,
            }
        )


class UserModelCreateDomain(BaseModel):
    name: str
    email: str
    password: str
    description: str
    contact_description: str
    image_upload: ImageUpload
    techs: Optional[list[int]] = None

    def model_dump(self):
        return clean_dict_return(
            {
                "name": self.name,
                "email": self.email,
                "password": self.password,
                "description": self.description,
                "contact_description": self.contact_description,
                "image_upload": self.image_upload.model_dump(),
                "techs": self.techs,
            }
        )


class UserModelUpdateDomain(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    description: Optional[str]
    contact_description: Optional[str]
    image_upload: Optional[ImageUpload]
    techs: Optional[list[int]] = None

    def model_dump(self):
        return clean_dict_return(
            {
                "name": self.name,
                "email": self.email,
                "password": self.password,
                "description": self.description,
                "contact_description": self.contact_description,
                "image_upload": (
                    self.image_upload.model_dump() if self.image_upload else None
                ),
                "techs": self.techs,
            }
        )
