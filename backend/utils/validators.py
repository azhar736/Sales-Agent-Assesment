from typing import Optional
import re
from pydantic import ValidationError
from models.company import Company
from models.product import Product


class InputValidator:
    @staticmethod
    def validate_company_data(data: dict) -> Optional[Company]:
        """
        Validate company input data
        """
        try:
            return Company(**data)
        except ValidationError:
            return None

    @staticmethod
    def validate_product_data(data: dict) -> Optional[Product]:
        """
        Validate product input data
        """
        try:
            return Product(**data)
        except ValidationError:
            return None

    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validate URL format
        """
        url_pattern = re.compile(
            r"^https?://"  # http:// or https://
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain...
            r"localhost|"  # localhost...
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
            r"(?::\d+)?"  # optional port
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )
        return url_pattern.match(url) is not None
