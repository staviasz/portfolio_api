from typing_extensions import Optional
from pydantic import BaseModel


class HttpRequest(BaseModel):
    headers: Optional[dict] = None
    body: Optional[dict] = None
    params: Optional[dict] = None
    query: Optional[dict] = None


class HttpResponse(BaseModel):
    status_code: int
    body: dict | list
