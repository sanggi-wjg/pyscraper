from decimal import Decimal

from pydantic import BaseModel, field_validator, Field, ConfigDict


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
