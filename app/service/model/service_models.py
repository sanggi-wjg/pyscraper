from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.enums.channel_enum import ChannelEnum


class ProductModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    channel: ChannelEnum
    channel_product_id: Optional[str]
    name: str
    url: Optional[str]
