import logging
from typing import List
from urllib.parse import urlencode

from bs4 import BeautifulSoup

from app.enums.channel_enum import ChannelEnum
from app.scraper.engine.scraper import BeautifulSoupScraper
from app.scraper.model.scraper_models import ScrapedProductModel

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
        return [
            ScrapedProductModel(
                channel_product_id=item.select_one("a")["data-content"],
                name=item.select_one(".tit").text,
                price=item.select_one(".price em").text,
                discount=None if not item.select_one(".disc") else item.select_one(".disc").text,
                url="https://aboutpet.co.kr/" + item.select_one("a")["href"],
            )
            for item in parser.select(".gd-item")
        ]
