import logging
from abc import ABC, abstractmethod
from typing import List, Optional, Dict

import httpx
from bs4 import BeautifulSoup

from app.enums.channel_enum import ChannelEnum
from app.scraper.model.scrape_result import ScrapeResult
from app.scraper.model.scraper_models import ScrapedProductModel
from app.util.util_header import get_fake_headers, get_fake_accept_language

logger = logging.getLogger(__name__)


class Scraper(ABC):

    def __init__(
        self,
        timeout: int = 10,
        headers: Optional[Dict[str, str]] = None,
        proxy: Optional[str] = None,
    ):
        self.fake_headers = get_fake_headers()
        self.fake_headers.update(
            {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Language": get_fake_accept_language(),
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
            }
        )
        self.proxy = proxy
        if headers:
            self.fake_headers.update(headers)
        self.timeout = timeout
        self.channel = None

    def _request_http_get(self, url: str) -> Optional[httpx.Response]:
        try:
            with httpx.Client(proxy=self.proxy, timeout=self.timeout) as client:
                response = client.get(url, headers=self.fake_headers)
                response.raise_for_status()
                return response
        except httpx.HTTPError as e:
            logger.error(f"Request error for URL {url}: {e}")
            return None

    @abstractmethod
    def scrape(self, q: str, **kwargs) -> ScrapeResult:
        raise NotImplementedError("Scraper is an abstract class and should not be instantiated directly.")


class HttpScraper(Scraper):

    @abstractmethod
    def _build_search_url(self, q: str) -> str:
        raise NotImplementedError("Scraper is an abstract class and should not be instantiated directly.")

    @abstractmethod
    def _transform(self, response: httpx.Response) -> List[ScrapedProductModel]:
        raise NotImplementedError("Scraper is an abstract class and should not be instantiated directly.")

    def scrape(self, q: str, **kwargs) -> ScrapeResult:
        if not self.channel:
            logger.error("Channel must be set for the scraper.")
            return ScrapeResult(False, ChannelEnum.VOID, [], "Channel must be set for the scraper.")
        if not q:
            logger.warning("Search query cannot be empty.")
            return ScrapeResult(False, self.channel, [], "Search query cannot be empty.")

        search_url = self._build_search_url(q)
        logger.info(f"Search URL: {search_url}")

        response = self._request_http_get(search_url)
        if response is None:
            logger.error(f"Failed to retrieve data from URL: {search_url}")
            return ScrapeResult(False, self.channel, [], "Failed to retrieve data from the URL.")

        try:
            extracted_products = self._transform(response)
            logger.info(f"Scraped: {extracted_products}")
            return ScrapeResult(True, self.channel, extracted_products, None)
        except Exception as e:
            logger.error(f"Error occurred while scraping: {e}")
            return ScrapeResult(False, self.channel, [], f"Error occurred while scraping: {e}")


class BeautifulSoupScraper(Scraper):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.beautiful_soup_features = "html.parser"

    @abstractmethod
    def _build_search_url(self, q: str) -> str:
        raise NotImplementedError("Scraper is an abstract class and should not be instantiated directly.")

    @abstractmethod
    def _extract(self, parser: BeautifulSoup, **kwargs) -> List[ScrapedProductModel]:
        raise NotImplementedError("Scraper is an abstract class and should not be instantiated directly.")

    def _get_parser(self, response: httpx.Response) -> BeautifulSoup:
        return BeautifulSoup(response.text, self.beautiful_soup_features)

    def scrape(self, q: str, **kwargs) -> ScrapeResult:
        if not self.channel:
            logger.error("Channel must be set for the scraper.")
            return ScrapeResult(False, ChannelEnum.VOID, [], "Channel must be set for the scraper.")
        if not q:
            logger.warning("Search query cannot be empty.")
            return ScrapeResult(False, self.channel, [], "Search query cannot be empty.")

        search_url = self._build_search_url(q)
        logger.info(f"Search URL: {search_url}")

        response = self._request_http_get(search_url)
        if response is None:
            logger.error(f"Failed to retrieve data from URL: {search_url}")
            return ScrapeResult(False, self.channel, [], "Failed to retrieve data from the URL.")

        try:
            parser = self._get_parser(response)
            extracted_products = self._extract(parser)
            logger.info(f"Scraped: {extracted_products}")
            return ScrapeResult(True, self.channel, extracted_products, None)
        except Exception as e:
            logger.error(f"Error occurred while scraping: {search_url}")
            return ScrapeResult(False, self.channel, [], f"Error occurred while scraping: {e}")
