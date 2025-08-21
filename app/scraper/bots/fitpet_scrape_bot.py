from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from app.scraper.engine.chrome_bot import HumanlikeChromeSeleniumBot


class FitpetMallScrapeBot(HumanlikeChromeSeleniumBot):
    HOME_URL = "https://fitpetmall.com/mall"

    """
    with FitpetMallScrapeBot() as bot:
    bot.search("로얄캐닌 독 미니 인도어 어덜트").scrape()
    """

    def search(self, query: str) -> "FitpetMallScrapeBot":
        self.get(self.HOME_URL)
        # self.human_mouse_movement()

        self.wait_and_click(By.CLASS_NAME, "search-placeholder")
        # self.behavior.random_delay()

        self.wait_and_type(By.CLASS_NAME, "SearchBarInputText__StyledInput-sc-cc34593b-1", query)
        search_box = self.find_element(By.CLASS_NAME, "SearchBarInputText__StyledInput-sc-cc34593b-1")
        search_box.send_keys(Keys.ENTER)

        # self.behavior.random_delay()
        # self.human_mouse_movement()
        return self

    def click_searched_product(self, index: int = 0) -> "FitpetMallScrapeBot":
        elements = self.find_elements(By.CLASS_NAME, "search-result-product-list__card")
        if elements and index < len(elements):
            self.human_click(elements[index])
        return self

    def scrape(self):
        elements = self.find_elements(By.CLASS_NAME, "search-result-product-list__card")

        for element in elements:
            name = element.find_element(By.CLASS_NAME, "CardBodyVertical__NameWrapper-sc-3b000831-1").text
            price_divs = element.find_element(
                By.CLASS_NAME, "CardBodyVertical__DefaultDiscountInfoWrapper-sc-3b000831-3"
            ).find_elements(By.CSS_SELECTOR, "div.Body1.Bold")

            if len(price_divs) == 1:
                price = price_divs[0].text
                discount = None
            elif len(price_divs) == 2:
                discount = price_divs[0].text
                price = price_divs[1].text
            else:
                continue

            print(name, "\t@\t", price, "\t@\t", discount)
