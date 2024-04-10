from typing_extensions import Optional
from pydantic import BaseModel, HttpUrl

from src.utils.clean_data_dict import clean_dict_return


class PostDomain(BaseModel):
    id: int
    name: str
    html: str
    user_id: int
    images_urls: Optional[list[HttpUrl]] = None
    techs: Optional[list[str]] = None

    def model_dump(self):
        return clean_dict_return(
            {
                "id": self.id,
                "name": self.name,
                "html": self.html,
                "images_urls": (
                    [str(url) for url in self.images_urls] if self.images_urls else None
                ),
                "user_id": self.user_id,
                "techs": self.techs,
            }
        )


class PostCreateModelDomain(BaseModel):
    name: str
    html: str
    images_urls: Optional[list[HttpUrl]] = None
    techs: Optional[list[int]] = None

    def model_dump(self):
        return clean_dict_return(
            {
                "name": self.name,
                "html": self.html,
                "images_urls": (
                    [str(url) for url in self.images_urls] if self.images_urls else None
                ),
                "techs": self.techs,
            }
        )


class PostUpdatesModelDomain(BaseModel):
    name: Optional[str]
    html: Optional[str]
    images_urls: Optional[list[HttpUrl]] = None
    techs: Optional[list[int]] = None

    def model_dump(self):
        return clean_dict_return(
            {
                "name": self.name,
                "html": self.html,
                "images_urls": (
                    [str(url) for url in self.images_urls] if self.images_urls else None
                ),
                "techs": self.techs,
            }
        )
