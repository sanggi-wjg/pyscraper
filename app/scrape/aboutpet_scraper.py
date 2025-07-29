import logging
from abc import ABC, abstractmethod
from typing import List, Optional
from urllib.parse import urlencode

import httpx
from bs4 import BeautifulSoup

from app.model.scrape_result import ScrapeResult
from app.model.scraped_product import ScrapedProduct
from app.util.util_user_agent import get_fake_headers

logger = logging.getLogger(__name__)


class Scraper(ABC):

    @abstractmethod
    def scrape(self, url: str, **kwargs) -> ScrapeResult:
        raise NotImplementedError()


class BeautifulSoupScraper(Scraper):

    def __init__(self, timeout: int = 30):
        self.beautiful_soup_features = "html.parser"
        self.fake_headers = get_fake_headers()
        self.fake_headers.update(
            {
                "Accept-Language": "ko,en-US;q=0.9,en;q=0.8",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            }
        )
        self.timeout = timeout

    def _make_request(self, url: str) -> Optional[httpx.Response]:
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(url, headers=self.fake_headers)
                response.raise_for_status()
                return response
        except httpx.RequestError as e:
            logger.error(f"Request error for URL {url}: {e}")
            return None

    def _get_parser(self, response: httpx.Response) -> BeautifulSoup:
        return BeautifulSoup(response.text, self.beautiful_soup_features)

    @abstractmethod
    def _build_search_url(self, q: str) -> str:
        raise NotImplementedError()

    @abstractmethod
    def _extract(self, parser: BeautifulSoup, **kwargs) -> List[ScrapedProduct]:
        raise NotImplementedError()

    def scrape(self, q: str, **kwargs) -> ScrapeResult:
        if not q:
            logger.warning("Search query cannot be empty.")
            return ScrapeResult(False, [], "Search query cannot be empty.")

        search_url = self._build_search_url(q)
        logger.info(f"Search URL: {search_url}")

        response = self._make_request(search_url)
        if response is None:
            logger.error(f"Failed to retrieve data from URL: {search_url}")
            return ScrapeResult(False, [], "Failed to retrieve data from the URL.")

        parser = self._get_parser(response)
        extracted_result = self._extract(parser)
        logger.info(f"Extracted result: {extracted_result}")
        return ScrapeResult(True, extracted_result, None)


class AboutPetScraper(BeautifulSoupScraper):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.endpoint = "https://aboutpet.co.kr/commonSearch"

    def _build_search_url(self, q: str) -> str:
        if not self.endpoint:
            raise ValueError("Endpoint must be set for the scraper.")

        query_string = urlencode(
            {"focus": 10, "cateCdL": 12565, "srchWord": q},
            safe="",
        )
        return f"{self.endpoint}?{query_string}"

    def _extract(self, parser: BeautifulSoup, **kwargs) -> List[ScrapedProduct]:
        return [
            ScrapedProduct(
                channel_product_id=item.select_one("a")["data-content"],
                name=item.select_one(".tit").text,
                price=item.select_one(".price em").text,
                discount=None if not item.select_one(".disc") else item.select_one(".disc").text,
                link=item.select_one("a")["href"],
            )
            for item in parser.select(".gd-item")
        ]
