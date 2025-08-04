from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, field_validator, Field, ConfigDict


class ScrapedProductModel(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str
    price: Decimal = Field(ge=0)
    discount: Optional[int] = Field(default=None, ge=0)
    channel_product_id: Optional[str] = Field(default=None)
    url: Optional[str] = Field(default=None)

    @field_validator("price", mode="before")
    @classmethod
    def convert_price(cls, value):
        if isinstance(value, str):
            value = value.replace("₩", "").replace(",", "").strip()

        try:
            return Decimal(value)
        except (ValueError, TypeError):
            raise ValueError("price must be a valid number.")

    @field_validator("discount", mode="before")
    @classmethod
    def convert_discount(cls, value):
        if not value:
            return None

        if isinstance(value, str):
            value = value.replace("%", "").strip()

        float_val = float(value)
        if 0 <= float_val <= 1:
            return int(float_val * 100)
        else:
            return int(float_val)

    @field_validator("channel_product_id", mode="before")
    @classmethod
    def convert_channel_product_id(cls, value):
        if isinstance(value, str):
            return value.strip()
        elif isinstance(value, int):
            return str(value)
        else:
            raise ValueError("channel_product_id must be a string or an integer.")
