from pydantic import BaseModel


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
