from typing import Dict, Any
import os
import json
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()


class LLMService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = AsyncOpenAI(api_key=self.api_key)
        self.model = "gpt-3.5-turbo-0125"  # Latest GPT-3.5 Turbo model
        self.temperature = 0.7
        self.max_tokens = 1000

    async def analyze_company(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze company data using GPT-3.5
        """
        try:
            prompt = self._create_company_analysis_prompt(company_data)
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert business analyst providing structured analysis of companies.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"},
            )
            return self._parse_openai_response(response)
        except Exception as e:
            raise Exception(f"Error analyzing company with OpenAI: {str(e)}")

    async def generate_sales_strategy(
        self, company_analysis: Dict[str, Any], product_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate sales strategy using GPT-3.5
        """
        try:
            prompt = self._create_sales_strategy_prompt(company_analysis, product_data)
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert sales strategist providing structured sales recommendations.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"},
            )
            return self._parse_openai_response(response)
        except Exception as e:
            raise Exception(f"Error generating sales strategy: {str(e)}")

    def _create_company_analysis_prompt(self, company_data: Dict[str, Any]) -> str:
        """Create a prompt for company analysis"""
        return f"""
        Analyze the following company information and provide detailed insights in JSON format:
        
        Company Information:
        - Name: {company_data.get('name', 'Unknown')}
        - Industry: {company_data.get('industry', 'Unknown')}
        - Description: {company_data.get('description', 'No description provided')}
        
        Please provide a JSON response with the following structure:
        {{
            "challenges": ["challenge1", "challenge2", ...],
            "opportunities": ["opportunity1", "opportunity2", ...],
            "marketPosition": "detailed market position analysis",
            "painPoints": ["point1", "point2", ...],
            "decisionFactors": ["factor1", "factor2", ...]
        }}
        """

    def _create_sales_strategy_prompt(
        self, company_analysis: Dict[str, Any], product_data: Dict[str, Any]
    ) -> str:
        """Create a prompt for sales strategy generation"""
        return f"""
        Based on the following information, generate a detailed sales strategy in JSON format:
        
        Company Analysis: {json.dumps(company_analysis, indent=2)}
        
        Product Information:
        - Name: {product_data.get('name', 'Unknown')}
        - Description: {product_data.get('description', 'No description provided')}
        - Price: {product_data.get('price', 'Unknown')}
        - Features: {', '.join(product_data.get('features', []))}
        
        Please provide a JSON response with the following structure:
        {{
            "valueProposition": "detailed value proposition",
            "keyPoints": ["point1", "point2", ...],
            "recommendedApproach": ["step1", "step2", ...],
            "potentialObjections": [
                {{"objection": "objection1", "response": "response1"}},
                {{"objection": "objection2", "response": "response2"}}
            ],
            "nextSteps": ["step1", "step2", ...]
        }}
        """

    def _parse_openai_response(self, response) -> Dict[str, Any]:
        """Parse OpenAI's response into structured data"""
        try:
            # Extract the content from the response
            content = response.choices[0].message.content
            # Parse JSON response
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise Exception(f"Error parsing JSON response: {str(e)}")
        except Exception as e:
            raise Exception(f"Error parsing OpenAI response: {str(e)}")
