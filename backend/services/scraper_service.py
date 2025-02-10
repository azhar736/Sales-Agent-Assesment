from typing import Dict, Any, Optional
import logging
import time
import re
from urllib.parse import urlparse
import aiohttp
from bs4 import BeautifulSoup
from cachetools import TTLCache
import validators
from aiohttp_client_cache import CachedSession, SQLiteBackend

logger = logging.getLogger(__name__)


class ScraperService:
    def __init__(self):
        self.cache = TTLCache(maxsize=100, ttl=3600)  # 1 hour cache
        self.rate_limit = 1  # seconds between requests
        self.last_request_time = 0
        self.headers = {
            "User-Agent": "Mozilla/5.0 (compatible; CompanyAnalyzer/1.0; +http://example.com)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }
        self.cache_backend = SQLiteBackend(
            cache_name="http_cache.sqlite",
            expire_after=3600,  # 1 hour cache
        )

    async def create_session(self) -> CachedSession:
        """Create a cached session with rate limiting"""
        return CachedSession(cache=self.cache_backend)

    async def scrape_company_info(self, company_url: str) -> Dict[str, Any]:
        """
        Scrape company information from given URL with caching and rate limiting
        """
        # Validate URL
        if not validators.url(company_url):
            raise ValueError(f"Invalid URL: {company_url}")

        # Check cache
        cache_key = f"company_info_{company_url}"
        if cache_key in self.cache:
            logger.info(f"Returning cached data for {company_url}")
            return self.cache[cache_key]

        # Rate limiting
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.rate_limit:
            await asyncio.sleep(self.rate_limit - time_since_last_request)

        try:
            async with await self.create_session() as session:
                self.last_request_time = time.time()
                async with session.get(company_url, headers=self.headers) as response:
                    if response.status != 200:
                        raise Exception(f"Failed to fetch URL: {response.status}")

                    html = await response.text()
                    soup = BeautifulSoup(html, "lxml")

                    # Extract company information
                    company_info = {
                        "title": self._extract_title(soup),
                        "description": self._extract_description(soup),
                        "contact_info": self._extract_contact_info(soup),
                        "social_links": self._extract_social_links(soup),
                        "metadata": self._extract_metadata(soup),
                        "company_details": self._extract_company_details(soup),
                    }

                    # Cache the results
                    self.cache[cache_key] = company_info
                    return company_info

        except Exception as e:
            logger.error(f"Error scraping {company_url}: {str(e)}")
            raise

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract company title from page"""
        title = soup.find("title")
        if not title:
            return ""
        # Clean and normalize the title
        return re.sub(r"\s+", " ", title.text.strip())

    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract company description from page"""
        # Try meta description first
        meta_desc = soup.find("meta", {"name": "description"})
        if meta_desc and meta_desc.get("content"):
            return meta_desc["content"].strip()

        # Try finding main content area
        main_content = soup.find(["main", "article"]) or soup
        paragraphs = main_content.find_all("p", limit=3)
        if paragraphs:
            return " ".join(p.text.strip() for p in paragraphs)
        return ""

    def _extract_contact_info(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract contact information"""
        contact_info = {}

        # Extract email addresses
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        emails = set()
        for text in soup.stripped_strings:
            found_emails = re.findall(email_pattern, text)
            emails.update(found_emails)
        if emails:
            contact_info["emails"] = list(emails)

        # Extract phone numbers
        phone_pattern = r"\+?[\d\s-]{10,}"
        phones = set()
        for text in soup.stripped_strings:
            found_phones = re.findall(phone_pattern, text)
            phones.update(found_phones)
        if phones:
            contact_info["phones"] = list(phones)

        # Extract address
        address_elements = soup.find_all(
            ["address", "div"], class_=lambda x: x and "address" in x.lower()
        )
        if address_elements:
            contact_info["address"] = address_elements[0].text.strip()

        return contact_info

    def _extract_social_links(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract social media links"""
        social_platforms = {
            "linkedin": r"linkedin\.com",
            "twitter": r"twitter\.com",
            "facebook": r"facebook\.com",
            "instagram": r"instagram\.com",
        }

        social_links = {}
        for link in soup.find_all("a", href=True):
            href = link["href"]
            for platform, pattern in social_platforms.items():
                if re.search(pattern, href, re.I):
                    social_links[platform] = href
        return social_links

    def _extract_metadata(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract page metadata"""
        metadata = {}

        # Extract Open Graph metadata
        og_tags = soup.find_all("meta", property=lambda x: x and x.startswith("og:"))
        for tag in og_tags:
            key = tag.get("property", "")[3:]  # Remove 'og:' prefix
            metadata[key] = tag.get("content", "")

        # Extract Twitter Card metadata
        twitter_tags = soup.find_all(
            "meta", name=lambda x: x and x.startswith("twitter:")
        )
        for tag in twitter_tags:
            key = tag.get("name", "")[8:]  # Remove 'twitter:' prefix
            metadata[key] = tag.get("content", "")

        return metadata

    def _extract_company_details(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract specific company details"""
        details = {}

        # Try to find company size/employee count
        employee_patterns = [
            r"(\d+(?:,\d+)?(?:\+)?\s+employees)",
            r"((?:small|medium|large)\s+company)",
        ]

        # Try to find industry information
        industry_section = soup.find(
            lambda tag: tag.name in ["div", "section"]
            and any(
                word in tag.text.lower() for word in ["industry", "sector", "about us"]
            )
        )
        if industry_section:
            details["industry"] = industry_section.text.strip()

        # Try to find founding year
        year_pattern = r"(?:founded|established|since)\s+in\s+(\d{4})"
        for text in soup.stripped_strings:
            year_match = re.search(year_pattern, text, re.I)
            if year_match:
                details["founded_year"] = year_match.group(1)
                break

        return details

    async def close(self):
        """Close the cache backend and any open sessions"""
        await self.cache_backend.close()
