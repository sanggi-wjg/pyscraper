from typing import List
from urllib.parse import urlencode

import httpx

from app.enums.channel_enum import ChannelEnum
from app.scraper.engine.scraper import HttpScraper
from app.scraper.model.scraper_models import ScrapedProductModel


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

    def _transform(self, response: httpx.Response) -> List[ScrapedProductModel]:
        resp = response.json()
        products = resp.get("products", [])
        return [
            ScrapedProductModel(
                channel_product_id=str(product["id"]),
                name=product["name"],
                price=product["price"],
                discount=product["discountRate"] if product.get("discountRate") else None,
                url=f"https://www.fitpetmall.com/mall/products/{product['id']}",
            )
            for product in products
        ]
