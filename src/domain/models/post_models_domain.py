from typing_extensions import Optional
from pydantic import BaseModel, HttpUrl


class PostDomain(BaseModel):
    id: int
    name: str
    html: str
    user_id: int
    images_urls: Optional[list[HttpUrl]]

    def model_dump(self):
        return {
            "id": self.id,
            "name": self.name,
            "html": self.html,
            "images_urls": (
                [str(url) for url in self.images_urls] if self.images_urls else []
            ),
            "user_id": self.user_id,
        }


class PostCreateModelDomain(BaseModel):
    name: str
    html: str
    images_urls: Optional[list[HttpUrl]]

    def model_dump(self):
        return {
            "name": self.name,
            "html": self.html,
            "images_urls": (
                [str(url) for url in self.images_urls] if self.images_urls else []
            ),
        }


class PostUpdatesModelDomain(BaseModel):
    name: Optional[str]
    html: Optional[str]
    images_urls: Optional[list[HttpUrl]]

    def model_dump(self):
        return {
            "name": self.name,
            "html": self.html,
            "images_urls": (
                [str(url) for url in self.images_urls] if self.images_urls else []
            ),
        }
