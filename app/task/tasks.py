import logging

from celery import shared_task

from app.scraper.sites.aboutpet_scraper import AboutPetScraper
from app.scraper.sites.fitpet_scraper import FitpetScraper
from app.service.product_service import ProductService
from app.util.util_proxy import get_working_proxy

logger = logging.getLogger(__name__)


@shared_task
def scrape_product_task():
    keyword = "하림더리얼"

    logger.info(f"[SCRAPE_PRODUCT_TASK] Start with {keyword}")
    proxy = get_working_proxy()
    if not proxy:
        logger.warning(f"[SCRAPE_PRODUCT_TASK] No available proxy found. Please check your proxy settings.")
        return

    service = ProductService()

    aboutpet_scrape_result = AboutPetScraper(proxy=proxy).scrape(keyword)
    service.create_or_update_product(aboutpet_scrape_result)

    fitpet_scrape_result = FitpetScraper(proxy=proxy).scrape(keyword)
    service.create_or_update_product(fitpet_scrape_result)

    logger.info(f"[SCRAPE_PRODUCT_TASK] Finished with {keyword}")
