import time
from urllib.parse import urlencode

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from app.scraper.engine.bot import HumanlikeSeleniumBot


class CoupangScrapeBot(HumanlikeSeleniumBot):
    HOME_URL = "https://www.coupang.com"
    SEARCH_URL = "https://www.coupang.com/np/search?"

    def roam_home(self) -> "CoupangScrapeBot":
        self.get(self.HOME_URL)
        self.human_mouse_movement()
        self.human_scroll()

        self.behavior.random_delay()
        self.human_scroll()
        self.human_scroll(direction="up")

        self.human_mouse_movement()
        self.human_scroll(direction="up")
        return self

    def search(self, query: str) -> "CoupangScrapeBot":
        self.wait_and_click(By.CLASS_NAME, "headerSearchKeyword")
        self.behavior.random_delay()

        self.wait_and_type(By.CLASS_NAME, "headerSearchKeyword", query)
        search_box = self.find_element(By.CLASS_NAME, "headerSearchKeyword")
        search_box.send_keys(Keys.ENTER)
        return self

    def search_2(self, query: str) -> "CoupangScrapeBot":
        query_string = urlencode({"q": query})
        self.get(f"{self.SEARCH_URL}?{query_string}")

        self.human_mouse_movement()
        self.human_scroll()

        self.behavior.random_delay()
        self.human_scroll()
        self.human_scroll(direction="up")
        self.human_scroll(direction="up")
        return self


with CoupangScrapeBot(driver_log_level="info", driver_path="/Applications/Firefox.app/Contents/MacOS/firefox") as bot:
    # bot.search_2("로얄캐닌 독 릴렉스 케어 파우치")
    bot.debug_detection().roam_home().debug_detection()
    time.sleep(20)

# print(urlencode({"q": "로얄캐닌 독 릴렉스 케어 파우치"}))
