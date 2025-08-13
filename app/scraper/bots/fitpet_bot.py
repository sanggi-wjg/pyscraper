import random
import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from app.scraper.engine.bot import HumanlikeSeleniumBot


class FitpetMallBot(HumanlikeSeleniumBot):
    HOME_URL = "https://fitpetmall.com/mall"

    def search(self, query: str) -> "FitpetMallBot":
        self.get(self.HOME_URL)
        self.human_mouse_movement(random.randint(1, 3))

        self.wait_and_click(By.CLASS_NAME, "search-placeholder")
        self.behavior.random_delay()

        self.wait_and_type(By.CLASS_NAME, "SearchBarInputText__StyledInput-sc-cc34593b-1", query)
        search_box = self.find_element(By.CLASS_NAME, "SearchBarInputText__StyledInput-sc-cc34593b-1")
        search_box.send_keys(Keys.ENTER)

        self.behavior.random_delay()
        self.human_mouse_movement(random.randint(1, 3))
        return self

    def click_searched_product(self, index: int = 0) -> "FitpetMallBot":
        elements = self.find_elements(By.CLASS_NAME, "search-result-product-list__card")
        if elements and index < len(elements):
            self.human_click(elements[index])
        return self


with FitpetMallBot() as fitpetmall:
    fitpetmall.search("유통기한").click_searched_product(0)
    time.sleep(5)
