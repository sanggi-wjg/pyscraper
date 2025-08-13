import logging
import random
import subprocess
from typing import Tuple, Dict, List, Union, Any

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from app.scraper.engine.bot_action_strategy import (
    HumanClickStrategy,
    HumanTypeStrategy,
    HumanScrollStrategy,
    HumanMouseMoveStrategy,
)
from app.scraper.engine.bot_behavior import HumanBehavior
from app.util.util_header import get_fake_firefox_user_agent

logger = logging.getLogger(__name__)


class BrowserConfig:

    def __init__(self):
        self.user_agent = get_fake_firefox_user_agent()
        # self.language = get_fake_accept_language()
        self.language = "ko,en-US;q=0.9,en;q=0.8"
        self.screen_size = random.choice(
            [
                (1920, 1080),
                (1366, 768),
                (1536, 864),
                (1440, 900),
            ]
        )


class HumanlikeSeleniumBot:
    """
    with HumanlikeSeleniumBot(speed_factor=1.5) as browser:
    (
        browser.get("https://fitpetmall.com/mall")
        .human_scroll(5)
        .random_mouse_movement(5)
        .human_scroll(direction="up")
        .random_mouse_movement(5)
        .take_screenshot("example.png")
    )

    """

    def __init__(
        self,
        geckodriver_path: str = "../driver/geckodriver",
        headless: bool = False,
        speed_factor: float = 1.0,
        profile_path: str | None = None,
        proxy: Dict[str, str] | None = None,
    ):

        self.geckodriver_path = geckodriver_path
        self.headless = headless
        self.behavior = HumanBehavior(speed_factor)
        self.profile_path = profile_path
        self.proxy = proxy
        self.driver: webdriver.Firefox | None = None

        self.click_strategy = HumanClickStrategy(self.behavior)
        self.type_strategy = HumanTypeStrategy(self.behavior)
        self.scroll_strategy = HumanScrollStrategy(self.behavior)
        self.mouse_move_strategy = HumanMouseMoveStrategy(self.behavior)

        self.browser_config = BrowserConfig()

    def _create_options(self) -> Options:
        options = Options()
        options.set_preference("general.useragent.override", self.browser_config.user_agent)
        # 자동화 탐지 방지
        options.set_preference("dom.webdriver.enabled", False)
        options.set_preference("useAutomationExtension", False)
        # 브라우저 설정
        options.set_preference("browser.startup.homepage", "about:blank")
        options.set_preference("startup.homepage_welcome_url", "about:blank")
        # 언어 설정
        options.set_preference("intl.accept_languages", self.browser_config.language)
        # 알림 및 미디어 비활성화
        options.set_preference("dom.push.enabled", False)
        options.set_preference("dom.notifications.enabled", False)
        options.set_preference("media.navigator.enabled", False)
        # 개인정보 보호
        options.set_preference("privacy.trackingprotection.enabled", True)
        options.set_preference("media.peerconnection.enabled", False)
        options.set_preference("geo.enabled", False)

        if self.headless:
            options.add_argument("--headless")

        if self.profile_path:
            options.set_preference("profile", self.profile_path)

        if self.proxy:
            self._setup_proxy(options)

        return options

    def _setup_proxy(self, options: Options) -> None:
        if self.proxy.get("http"):
            proxy_parts = self.proxy["http"].split(":")
            options.set_preference("network.proxy.type", 1)
            options.set_preference("network.proxy.http", proxy_parts[0])
            options.set_preference("network.proxy.http_port", int(proxy_parts[1]))
            options.set_preference("network.proxy.ssl", proxy_parts[0])
            options.set_preference("network.proxy.ssl_port", int(proxy_parts[1]))

    def start(self) -> "HumanlikeSeleniumBot":
        if self.driver:
            return self

        try:
            options = self._create_options()
            service = Service(
                self.geckodriver_path,
                log_output=subprocess.STDOUT,
                service_args=["--log", "info"],
            )

            width, height = self.browser_config.screen_size
            self.driver = webdriver.Firefox(service=service, options=options)
            self.driver.set_window_size(width, height)
            self._hide_automation_properties()
            return self

        except Exception as e:
            raise Exception(f"브라우저 시작 실패: {e}")

    def _hide_automation_properties(self) -> None:
        # 자동화 속성 숨기기
        script = """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
        });
        
        delete navigator.__proto__.webdriver;
        
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5],
        });
        
        Object.defineProperty(navigator, 'languages', {
            get: () => ['ko-KR', 'ko', 'en-US', 'en'],
        });
        
        // WebGL 설정
        const getParameter = WebGLRenderingContext.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(parameter) {
            if (parameter === 37445) {
                return 'Intel Inc.';
            }
            if (parameter === 37446) {
                return 'Intel Iris OpenGL Engine';
            }
            return getParameter(parameter);
        };
        """
        self.driver.execute_script(script)

    def get(self, url: str) -> "HumanlikeSeleniumBot":
        if not self.driver:
            raise Exception("브라우저가 시작되지 않았습니다. start() 메서드를 먼저 호출하세요.")

        self.driver.get(url)
        self.behavior.random_delay(1, 5)
        return self

    def find_element(self, by: str, value: str, timeout: int = 10) -> WebElement | None:
        try:
            element = WebDriverWait(self.driver, timeout).until(
                expected_conditions.presence_of_element_located((by, value)),
            )
            return element
        except TimeoutException:
            logger.warning(f"no such element. {by}={value}")
            return None

    def find_elements(self, by: str, value: str, timeout: int = 10) -> List[WebElement]:
        try:
            WebDriverWait(self.driver, timeout).until(
                expected_conditions.presence_of_element_located((by, value)),
            )
            return self.driver.find_elements(by, value)
        except TimeoutException:
            logger.warning(f"no such element. {by}={value}")
            return []

    def human_click(self, element: WebElement) -> "HumanlikeSeleniumBot":
        if isinstance(element, tuple):
            element = self.find_element(element[0], element[1])

        self.click_strategy.execute(self.driver, element)
        self.behavior.random_delay(0.5, 2.0)
        return self

    def human_type(
        self,
        element: Union[WebElement, Tuple[By, str]],
        text: str,
        clear: bool = True,
    ) -> "HumanlikeSeleniumBot":
        if isinstance(element, tuple):
            element = self.find_element(element[0], element[1])

        self.type_strategy.execute(self.driver, element, text=text, clear=clear)
        self.behavior.random_delay(0.3, 1.0)
        return self

    def human_scroll(self, scrolls: int = 5, direction: str = "down") -> "HumanlikeSeleniumBot":
        self.scroll_strategy.execute(self.driver, element=None, scrolls=scrolls, direction=direction)
        return self

    def human_mouse_movement(self, movements: int = 5) -> "HumanlikeSeleniumBot":
        self.mouse_move_strategy.execute(self.driver, element=None, movements=movements)
        return self

    def wait_and_click(
        self,
        by: str,
        value: str,
        timeout: int = 10,
    ) -> "HumanlikeSeleniumBot":
        element = self.find_element(by, value, timeout)
        return self.human_click(element)

    def wait_and_type(
        self,
        by: str,
        value: str,
        text: str,
        timeout: int = 10,
        clear: bool = True,
    ) -> "HumanlikeSeleniumBot":
        element = self.find_element(by, value, timeout)
        return self.human_type(element, text, clear)

    def take_screenshot(self, filename: str) -> "HumanlikeSeleniumBot":
        self.driver.save_screenshot(filename)
        return self

    def execute_script(self, script: str, *args) -> Any:
        return self.driver.execute_script(script, *args)

    def get_page_source(self) -> str:
        return self.driver.page_source

    def get_current_url(self) -> str:
        return self.driver.current_url

    def back(self) -> "HumanlikeSeleniumBot":
        self.driver.back()
        self.behavior.random_delay(1, 2)
        return self

    def forward(self) -> "HumanlikeSeleniumBot":
        self.driver.forward()
        self.behavior.random_delay(1, 2)
        return self

    def refresh(self) -> "HumanlikeSeleniumBot":
        self.driver.refresh()
        self.behavior.random_delay(2, 4)
        return self

    def switch_to_window(self, window_handle: str) -> "HumanlikeSeleniumBot":
        self.driver.switch_to.window(window_handle)
        self.behavior.random_delay(0.5, 1.0)
        return self

    def close_current_window(self) -> "HumanlikeSeleniumBot":
        self.driver.close()
        return self

    def quit(self) -> None:
        if self.driver:
            self.behavior.random_delay(0.5, 1.5)
            self.driver.quit()
            self.driver = None

    def __enter__(self):
        return self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()
