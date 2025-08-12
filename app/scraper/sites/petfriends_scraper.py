import logging
from typing import List
from urllib.parse import urlencode

from bs4 import BeautifulSoup

from app.enums.channel_enum import ChannelEnum
from app.scraper.engine.scraper import BeautifulSoupScraper
from app.scraper.model.scraper_models import ScrapedProductModel

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
        result = []
        for item in parser.select("ul.c-hdwPLF > li"):
            name = item.select_one("h1.c-lhSsmZ")
            price = item.select_one("em.c-lhSsmZ")
            discount = item.select_one("strong.c-esKGUC")
            url = item.select_one("a").get("href")
            if not name or not price:
                logger.info("Missing required fields in the scraped item.")
                continue

            result.append(
                ScrapedProductModel(
                    channel_product_id=None,
                    name=name.text,
                    price=price.text,
                    discount=None if not discount else discount.text,
                    url="https://m.pet-friends.co.kr" + url,
                )
            )
        return result
