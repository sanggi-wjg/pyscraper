import logging

from selenium.webdriver.chrome.options import Options
from seleniumbase import Driver

from app.scraper.engine.bot import HumanlikeSeleniumBot

logger = logging.getLogger(__name__)


class HumanlikeChromeSeleniumBot(HumanlikeSeleniumBot):

    def __init__(
        self,
        driver_path: str = "../driver/chromedriver",
        driver_log_level: str = "info",
        use_tor_proxy: bool = False,
        headless: bool = False,
        speed_factor: float = 1.0,
        profile_path: str | None = None,
    ):
        super().__init__(
            driver_path,
            driver_log_level,
            use_tor_proxy,
            headless,
            speed_factor,
            profile_path,
        )

    def start(self) -> "HumanlikeSeleniumBot":
        if self.driver:
            return self

        try:
            self.driver = Driver(browser="chrome", uc=True)
            return self

        except Exception as e:
            raise Exception(f"브라우저 시작 실패: {e}")

    def _create_options(self) -> Options:
        pass

    def _hide_automation_properties(self) -> None:
        pass
