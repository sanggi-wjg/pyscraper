import logging
import random
import time

from celery import shared_task

from app.scraper.engine.chrome_bot import HumanlikeChromeSeleniumBot
from app.scraper.sites.aboutpet_scraper import AboutPetScraper
from app.scraper.sites.fitpet_scraper import FitpetScraper
from app.scraper.sites.petfriends_scraper import PetFriendsScraper
from app.service.keyword_service import KeywordService
from app.service.product_service import ProductService

logger = logging.getLogger(__name__)


@shared_task
def scrape_products_task():
    logger.info("[SCRAPE_PRODUCTS_TASK] 🚀 Start 🚀")
    # proxy = get_working_proxy()
    # if not proxy:
    #     logger.warning("[SCRAPE_PRODUCTS_TASK] No available proxy found. If this situation continues, please check your proxy settings.")
    #     return

    keyword_service = KeywordService()
    keywords = keyword_service.get_available_keywords()
    logger.info(f"[SCRAPE_PRODUCTS_TASK] Scraping products... Size of keywords: {len(keywords)}")
    if not keywords:
        return

    for keyword in keywords:
        scrape_product_by_keyword_task.delay(keyword.id, keyword.word)
        time.sleep(random.randint(1, 10))

    logger.info("[SCRAPE_PRODUCTS_TASK] 😎 Finished 😎")


@shared_task
def scrape_product_by_keyword_task(keyword_id: int, keyword_word: str):
    logger.info(f"[SCRAPE_PRODUCT_TASK_WITH_KEYWORD] Start with {keyword_word}")
    service = ProductService()

    service.sync_product(AboutPetScraper().scrape(keyword_word), keyword_id)
    service.sync_product(FitpetScraper().scrape(keyword_word), keyword_id)
    service.sync_product(PetFriendsScraper().scrape(keyword_word), keyword_id)

    logger.info(f"[SCRAPE_PRODUCT_TASK_WITH_KEYWORD] Finished with {keyword_word}")


@shared_task
def debug_chrome_bot():
    logger.info("[DEBUG_CHROME_BOT] 🚀 Start 🚀")
    with HumanlikeChromeSeleniumBot() as bot:
        (
            bot.get("https://sanggi-jayg.tistory.com/")
            .human_scroll()
            .debug_detection()
            .human_mouse_movement()
            .human_scroll()
            .debug_antibot(take_screenshot=False)
            .debug_detection()
        )
    logger.info("[DEBUG_CHROME_BOT] 😎 Finished 😎")
