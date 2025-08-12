import datetime
import decimal
from typing import List

from pydantic import BaseModel, ConfigDict

from app.enums.channel_enum import ChannelEnum


class ProductPriceModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    price: decimal.Decimal
    discount: decimal.Decimal | None
    created_at: datetime.datetime
    product_id: int


class ProductModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    channel: ChannelEnum
    channel_product_id: str | None
    name: str
    url: str | None
    created_at: datetime.datetime
    prices: List[ProductPriceModel]


class KeywordModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    word: str
    created_at: datetime.datetime
