from pydantic import BaseModel
from typing import Dict, Any


class Analysis(BaseModel):
    company_id: str
    product_id: str
    analysis: Dict[str, Any]
    strategy: Dict[str, Any]
    confidence_score: float = 0.0
