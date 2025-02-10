from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class Product(BaseModel):
    id: str
    name: str
    description: str
    price: Decimal
    category: Optional[str] = None
    features: list[str] = []
