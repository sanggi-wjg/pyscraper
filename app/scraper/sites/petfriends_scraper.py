import logging
from typing import List
from urllib.parse import urlencode

from bs4 import BeautifulSoup

from app.enums.channel_enum import ChannelEnum
from app.scraper.engine.scraper import BeautifulSoupScraper
from app.scraper.model.scraper_models import ScrapedProductModel
from app.util.util_scrape import safe_extract_text, safe_extract_attr

logger = logging.getLogger(__name__)


class PetFriendsScraper(BeautifulSoupScraper):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.endpoint = "https://m.pet-friends.co.kr/search/1/result"
        self.channel = ChannelEnum.PET_FRIENDS

    def _build_search_url(self, q: str) -> str:
        if not self.endpoint:
            raise ValueError("Endpoint must be set for the scraper.")

        query_string = urlencode(
            {
                "word": q,
            },
            safe="",
        )
        return f"{self.endpoint}?{query_string}"

    def _extract(self, parser: BeautifulSoup, **kwargs) -> List[ScrapedProductModel]:
        items = parser.select("ul.c-hdwPLF > li")
        if not items:
            logger.info("No items found in the HTML.")
            return []

        result = []

        for item in items:
            name = safe_extract_text(item, "h1.c-lhSsmZ")
            price = safe_extract_text(item, "em.c-lhSsmZ")
            discount = safe_extract_text(item, "strong.c-esKGUC")
            url = safe_extract_attr(item, "a", "href")

            if not all([name, price]):
                continue

            result.append(
                ScrapedProductModel(
                    channel_product_id=None,
                    name=name,
                    price=price,
                    discount=discount,
                    url="https://m.pet-friends.co.kr" + url,
                )
            )
        return result
