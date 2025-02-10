from pydantic import BaseModel, HttpUrl
from typing import Optional


class Company(BaseModel):
    id: str
    name: str
    website: HttpUrl
    industry: Optional[str] = None
    size: Optional[str] = None
    description: Optional[str] = None
