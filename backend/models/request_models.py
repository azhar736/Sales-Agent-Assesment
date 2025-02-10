from pydantic import BaseModel, HttpUrl, constr, confloat
from typing import Optional
from fastapi import UploadFile


class AnalysisRequest(BaseModel):
    productName: constr(min_length=1)
    productDescription: constr(min_length=1)
    price: confloat(gt=0)
    companyUrl: str
    competitors: Optional[str] = None
    additionalNotes: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "productName": "AI Analytics Platform",
                "productDescription": "Advanced analytics solution",
                "price": 999.99,
                "companyUrl": "https://www.example.com",
                "competitors": "competitor1.com\ncompetitor2.com",
                "additionalNotes": "Target market: Enterprise businesses",
            }
        }
