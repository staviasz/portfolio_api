from typing_extensions import Optional
from pydantic import BaseModel


class HttpRequest(BaseModel):
    headers: Optional[dict]
    body: Optional[dict]
    params: Optional[dict]
    query: Optional[dict]


class HttpResponse(BaseModel):
    status_code: int
    body: dict | list[dict]
