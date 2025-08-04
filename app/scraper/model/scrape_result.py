from dataclasses import dataclass
from typing import List, Optional

from app.enums.channel_enum import ChannelEnum
from app.scraper.model.scraper_models import ScrapedProductModel


@dataclass(frozen=True, slots=True)
class ScrapeResult:
    is_success: bool
    channel: ChannelEnum
    dataset: List[ScrapedProductModel]
    error_message: Optional[str]
