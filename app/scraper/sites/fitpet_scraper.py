from typing import List
from urllib.parse import urlencode

import httpx

from app.enums.channel import ChannelEnum
from app.scraper.engine.scraper import HttpScraper
from app.scraper.model.scraped_product import ScrapedProduct


class FitpetScraper(HttpScraper):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.endpoint = "https://api-v4.fitpet.kr/api/v3/products/search"
        self.channel = ChannelEnum.FITPET

    def _build_search_url(self, q: str) -> str:
        if not self.endpoint:
            raise ValueError("Endpoint must be set for the scraper.")

        query_string = urlencode(
            {
                "keyword": q,
                "petType": "DOG",
                "includeSoldOut": True,
                "sortBy": "MD_RECOMMENDED",
                "sortDirection": "ASC",
                "size": 30,
                "page": 1,
            },
            safe="",
        )
        return f"{self.endpoint}?{query_string}"

    def _extract(self, response: httpx.Response) -> List[ScrapedProduct]:
        resp = response.json()
        products = resp.get("products", [])
        return [
            ScrapedProduct(
                channel_product_id=product["id"],
                name=product["name"],
                price=product["price"],
                discount=product["discountRate"] if product.get("discountRate") else None,
                link=f"https://www.fitpetmall.com/mall/products/{product['id']}",
            )
            for product in products
        ]
