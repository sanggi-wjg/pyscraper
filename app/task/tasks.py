import logging

from celery import shared_task

from app.scraper.sites.aboutpet_scraper import AboutPetScraper
from app.scraper.sites.fitpet_scraper import FitpetScraper
from app.service.keyword_service import KeywordService
from app.service.product_service import ProductService
from app.util.util_proxy import get_working_proxy

logger = logging.getLogger(__name__)


@shared_task
def scrape_products_task():
    logger.info("[SCRAPE_PRODUCTS_TASK] 🚀 Start 🚀")
    proxy = get_working_proxy()
    if not proxy:
        logger.warning(
            "[SCRAPE_PRODUCTS_TASK] No available proxy found. If this situation continues, please check your proxy settings."
        )
        return

    keyword_service = KeywordService()
    keywords = keyword_service.get_all_keywords()
    logger.info(f"[SCRAPE_PRODUCTS_TASK] Scraping products... Size of keywords: {len(keywords)}")
    if not keywords:
        return
    for keyword in keywords:
        scrape_product_task_with_keyword.delay(proxy, keyword.id, keyword.word)

    logger.info("[SCRAPE_PRODUCTS_TASK] 😎 Finished 😎")


@shared_task
def scrape_product_task_with_keyword(proxy: str, keyword_id: int, keyword_word: str):
    logger.info(f"[SCRAPE_PRODUCT_TASK_WITH_KEYWORD] Start with {keyword_word}")
    service = ProductService()

    aboutpet_scrape_result = AboutPetScraper(proxy=proxy).scrape(keyword_word)
    service.sync_product(aboutpet_scrape_result, keyword_id)

    fitpet_scrape_result = FitpetScraper(proxy=proxy).scrape(keyword_word)
    service.sync_product(fitpet_scrape_result, keyword_id)

    logger.info(f"[SCRAPE_PRODUCT_TASK_WITH_KEYWORD] Finished with {keyword_word}")
