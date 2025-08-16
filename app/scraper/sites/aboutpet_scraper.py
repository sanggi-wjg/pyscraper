import logging
from typing import List
from urllib.parse import urlencode

from bs4 import BeautifulSoup

from app.enums.channel_enum import ChannelEnum
from app.scraper.engine.scraper import BeautifulSoupScraper
from app.scraper.model.scraper_models import ScrapedProductModel
from app.util.util_scrape import safe_extract_text, safe_extract_attr

logger = logging.getLogger(__name__)


class AboutPetScraper(BeautifulSoupScraper):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.endpoint = "https://aboutpet.co.kr/commonSearch"
        self.channel = ChannelEnum.ABOUT_PET

    def _build_search_url(self, q: str) -> str:
        if not self.endpoint:
            raise ValueError("Endpoint must be set for the scraper.")

        query_string = urlencode(
            {
                "srchWord": q,
                "focus": 10,
                "cateCdL": 12565,
            },
            safe="",
        )
        return f"{self.endpoint}?{query_string}"

    def _extract(self, parser: BeautifulSoup, **kwargs) -> List[ScrapedProductModel]:
        items = parser.select(".gd-item")
        if not items:
            logger.info("No items found in the HTML.")
            return []

        result = []

        for item in items:
            name = safe_extract_text(item, ".tit")
            price = safe_extract_text(item, ".price em")
            discount = safe_extract_text(item, ".disc")
            url = safe_extract_attr(item, "a", "href")
            channel_product_id = safe_extract_attr(item, "a", "data-content")

            if not all([name, price]):
                continue

            result.append(
                ScrapedProductModel(
                    channel_product_id=channel_product_id,
                    name=name,
                    price=price,
                    discount=discount,
                    url="https://aboutpet.co.kr/" + url,
                )
            )
        return result
