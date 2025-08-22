import logging
from decimal import Decimal

from pydantic import BaseModel, field_validator, Field, ConfigDict

from app.util.util_scrape import to_decimal, clean_price_text, clean_discount_text, to_discount_percent

logger = logging.getLogger(__name__)


class ScrapedProductModel(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str
    price: Decimal = Field(ge=0)
    discount: int | None = Field(default=None, ge=0)
    channel_product_id: str | None = Field(default=None)
    url: str | None = Field(default=None)

    @field_validator("price", mode="before")
    @classmethod
    def convert_price(cls, value):
        if isinstance(value, str):
            value = clean_price_text(value)

        return to_decimal(value)

    @field_validator("discount", mode="before")
    @classmethod
    def convert_discount(cls, value):
        if not value:
            return None

        if isinstance(value, str):
            value = clean_discount_text(value)

        return to_discount_percent(value)
