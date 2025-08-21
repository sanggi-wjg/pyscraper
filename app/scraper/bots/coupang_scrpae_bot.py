from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from app.enums.channel_enum import ChannelEnum
from app.scraper.engine.chrome_bot import HumanlikeChromeSeleniumBot
from app.scraper.model.scrape_result import ScrapeResult
from app.scraper.model.scraper_models import ScrapedProductModel
from app.util.util_scrape import safe_extract_text_by_bot, safe_extract_attr_by_bot, clean_url_text


class CoupangScrapeBot(HumanlikeChromeSeleniumBot):
    HOME_URL = "https://www.coupang.com"

    def roam_home(self) -> "CoupangScrapeBot":
        self.get(self.HOME_URL)
        self.human_mouse_movement()
        self.behavior.random_delay()
        return self

    def go_home(self):
        self.get(self.HOME_URL)
        self.human_mouse_movement()
        return self

    def search(self, query: str) -> "CoupangScrapeBot":
        self.wait_and_click(By.CLASS_NAME, "headerSearchKeyword")
        self.behavior.random_delay()

        self.wait_and_type(By.CLASS_NAME, "headerSearchKeyword", query)
        search_box = self.find_element(By.CLASS_NAME, "headerSearchKeyword")
        if not search_box:
            return self

        search_box.send_keys(Keys.ENTER)
        return self

    def click_searched_product(self, index: int = 0) -> "CoupangScrapeBot":
        elements = self.find_elements(By.CLASS_NAME, "ProductUnit_productUnit__Qd6sv")
        if elements and index < len(elements):
            self.human_click(elements[index])
        return self

    def scrape(self) -> ScrapeResult:
        self.human_mouse_movement()
        elements = self.find_elements(By.CLASS_NAME, "ProductUnit_productUnit__Qd6sv")
        result = []

        for element in elements:
            channel_product_id = element.get_attribute("data-id")
            name = safe_extract_text_by_bot(element, By.CLASS_NAME, "ProductUnit_productName__gre7e")
            if not name:
                name = safe_extract_text_by_bot(element, By.CLASS_NAME, "ProductUnit_productNameV2__cV9cw")
            discount = safe_extract_text_by_bot(element, By.CLASS_NAME, "PriceInfo_discountRate__EsQ8I")
            price = safe_extract_text_by_bot(element, By.CLASS_NAME, "Price_salePrice__P6Mfd")
            url = safe_extract_attr_by_bot(element, By.CSS_SELECTOR, "a", "href")

            result.append(
                ScrapedProductModel(
                    channel_product_id=channel_product_id,
                    name=name,
                    price=price,
                    discount=discount,
                    url=clean_url_text(url),
                )
            )

        return ScrapeResult(True, ChannelEnum.COUPANG, result, None)
