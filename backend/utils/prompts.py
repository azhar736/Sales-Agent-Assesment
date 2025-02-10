COMPANY_ANALYSIS_PROMPT = """
Analyze the following company information and provide insights:
Company: {company_name}
Industry: {industry}
Description: {description}

Please provide:
1. Key business challenges
2. Potential pain points
3. Decision-making factors
"""

SALES_STRATEGY_PROMPT = """
Based on the company analysis and product information, generate a sales strategy:
Company Analysis: {company_analysis}
Product: {product_name}
Price: {price}
Features: {features}

Generate:
1. Value proposition
2. Key selling points
3. Recommended approach
"""
