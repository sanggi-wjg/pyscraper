from dataclasses import dataclass
from typing import List, Optional

from app.enums.channel_enum import ChannelEnum
from app.scraper.model.scraped_product import ScrapedProduct


@dataclass(frozen=True, slots=True)
class ScrapeResult:
    is_success: bool
    channel: ChannelEnum
    dataset: List[ScrapedProduct]
    error_message: Optional[str]
