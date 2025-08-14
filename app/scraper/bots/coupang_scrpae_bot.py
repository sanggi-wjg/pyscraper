from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from app.scraper.engine.chrome_bot import HumanlikeChromeSeleniumBot


class CoupangScrapeBot(HumanlikeChromeSeleniumBot):
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

# with CoupangScrapeBot(driver_log_level="info", driver_path="/Applications/Firefox.app/Contents/MacOS/firefox") as bot:
#     bot.debug_detection().roam_home().debug_detection().search("로얄캐닌 독 릴렉스 케어 파우치")
#     time.sleep(20)
