import logging
import random
import time
from typing import List

from celery import shared_task
from celery_once import QueueOnce

from app.config.celery import app
from app.scraper.bots.coupang_scrpae_bot import CoupangScrapeBot
from app.scraper.engine.chrome_bot import HumanlikeChromeSeleniumBot
from app.scraper.sites.aboutpet_scraper import AboutPetScraper
from app.scraper.sites.fitpet_scraper import FitpetScraper
from app.scraper.sites.petfriends_scraper import PetFriendsScraper
from app.service.keyword_service import KeywordService
from app.service.model.service_models import KeywordModel
from app.service.product_service import ProductService

logger = logging.getLogger(__name__)


@app.task(base=QueueOnce, once={"graceful": True, "timeout": 60 * 60})
def scrape_products_task():
    logger.info("[SCRAPE_PRODUCTS_TASK] 🚀 Start 🚀")
    # proxy = get_working_proxy()
    # if not proxy:
    #     logger.warning("[SCRAPE_PRODUCTS_TASK] No available proxy found. If this situation continues, please check your proxy settings.")
    #     return

    keywords = _get_keywords()
    if not keywords:
        return

    for keyword in keywords:
        scrape_product_by_keyword_task.delay(keyword.id, keyword.word)
        time.sleep(random.randint(1, 10))

    logger.info("[SCRAPE_PRODUCTS_TASK] 😎 Finished 😎")


@shared_task
def scrape_product_by_keyword_task(keyword_id: int, keyword_word: str):
    logger.info(f"[SCRAPE_PRODUCT_TASK_WITH_KEYWORD] Start with {keyword_word}")
    product_service = ProductService()

    product_service.sync_product(AboutPetScraper().scrape(keyword_word), keyword_id)
    product_service.sync_product(FitpetScraper().scrape(keyword_word), keyword_id)
    product_service.sync_product(PetFriendsScraper().scrape(keyword_word), keyword_id)

    logger.info(f"[SCRAPE_PRODUCT_TASK_WITH_KEYWORD] Finished with {keyword_word}")


@app.task(base=QueueOnce, once={"graceful": True, "timeout": 60 * 60})
def scrape_products_task_by_bot():
    # if random.randint(0, 1) % 2 == 0:
    #     return
    logger.info("[SCRAPE_PRODUCTS_TASK_BY_BOT] 🚀 Start 🚀")

    keywords = _get_keywords()
    if not keywords:
        return

    product_service = ProductService()

    bot: CoupangScrapeBot
    with CoupangScrapeBot() as bot:
        bot = bot.go_home()

        for keyword in keywords:
            scrape_result = bot.search(keyword.word).scrape()
            bot.human_scroll().human_mouse_movement()
            product_service.sync_product(scrape_result, keyword.id)

    logger.info("[SCRAPE_PRODUCTS_TASK_BY_BOT] 😎 Finished 😎")


@app.task(base=QueueOnce, once={"graceful": True, "timeout": 60 * 60})
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


def _get_keywords() -> List[KeywordModel]:
    keyword_service = KeywordService()
    keywords = keyword_service.get_available_keywords()
    logger.info(f"Scraping products... Size of keywords: {len(keywords)}")
    return keywords
