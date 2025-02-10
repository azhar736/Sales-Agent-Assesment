from typing import Dict, Any, Optional
from .llm_service import LLMService
from .scraper_service import ScraperService
from models.company import Company
from models.product import Product
from models.analysis import Analysis
import validators


class AnalysisService:
    def __init__(self):
        self.llm_service = LLMService()
        self.scraper_service = ScraperService()

    async def analyze_sales_opportunity(
        self, company: Company, product: Product
    ) -> Analysis:
        """
        Analyze sales opportunity for a given company and product
        """
        company_data = await self.scraper_service.scrape_company_info(company.website)
        company_analysis = await self.llm_service.analyze_company(company_data)
        sales_strategy = await self.llm_service.generate_sales_strategy(
            company_analysis, product.dict()
        )

        return Analysis(
            company_id=company.id,
            product_id=product.id,
            analysis=company_analysis,
            strategy=sales_strategy,
        )

    async def analyze(
        self, data: Dict[str, Any], file_content: Optional[bytes] = None
    ) -> Dict[str, Any]:
        # Validate data
        if not data.get("productName"):
            raise ValueError("Product name is required")

        if not data.get("productDescription"):
            raise ValueError("Product description is required")

        if not data.get("price") or float(data["price"]) <= 0:
            raise ValueError("Valid price is required")

        if not data.get("companyUrl"):
            raise ValueError("Company URL is required")

        # Validate URL format
        if not validators.url(data["companyUrl"]):
            raise ValueError(f"Invalid URL: {data['companyUrl']}")

        # Process the analysis
        # ... rest of your analysis logic ...

        return {
            "companyAnalysis": {
                "challenges": ["Challenge 1", "Challenge 2"],
                "opportunities": ["Opportunity 1", "Opportunity 2"],
                "marketPosition": "Market Position",
            },
            "salesStrategy": {
                "valueProposition": "Value Proposition",
                "keyPoints": ["Key Point 1", "Key Point 2"],
                "recommendations": ["Recommendation 1", "Recommendation 2"],
            },
        }
