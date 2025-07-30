from typing import Optional

from pydantic import BaseModel, field_validator, Field


class ScrapedProduct(BaseModel):
    channel_product_id: Optional[str] = Field(default=None)
    name: str
    price: str
    discount: Optional[str] = Field(default=None)
    link: Optional[str] = Field(default=None)

    @classmethod
    @field_validator("name")
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError("name must not be empty")
        return v.strip()
