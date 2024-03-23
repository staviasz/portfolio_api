from pydantic import BaseModel, Field
from src.presentation.types.image_upload_type_presentation import ImageUpload


class UploadImageSchema(BaseModel):
    images_uploads: ImageUpload | list[ImageUpload] = Field(...)
    folder_name: str = Field(..., min_length=5, max_length=20)
