import datetime
import logging
import random
import subprocess
import time
from typing import List, Union

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from seleniumbase.core import sb_driver

from app.scraper.engine.bot_action_strategy import (
    HumanClickStrategy,
    HumanTypeStrategy,
    HumanScrollStrategy,
    HumanMouseMoveStrategy,
    SeleniumBotActionStrategy,
)
from app.scraper.engine.bot_behavior import HumanBehavior, SeleniumBotBehavior
from app.util.util_header import get_fake_firefox_user_agent

logger = logging.getLogger(__name__)


class BotBrowserConfig:

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
        driver_path: str = "../driver/geckodriver",
        driver_log_level: str = "info",
        use_tor_proxy: bool = False,
        headless: bool = False,
        speed_factor: float = 1.0,
        profile_path: str | None = None,
    ):
        """
        use_tor_proxy True 경우, tor 설치 및 실행 후 동작해야 합니다
        - Mac: `brew install tor`
        """
        self.driver_path = driver_path
        self.driver_log_level = driver_log_level
        self.use_tor_proxy = use_tor_proxy
        self.headless = headless
        self.profile_path = profile_path
        self.behavior: SeleniumBotBehavior = HumanBehavior(speed_factor)
        self.driver: Union[webdriver.Firefox, sb_driver.DriverMethods, None] = None

        self.click_strategy: SeleniumBotActionStrategy = HumanClickStrategy(self.behavior)
        self.type_strategy: SeleniumBotActionStrategy = HumanTypeStrategy(self.behavior)
        self.scroll_strategy: SeleniumBotActionStrategy = HumanScrollStrategy(self.behavior)
        self.mouse_move_strategy: SeleniumBotActionStrategy = HumanMouseMoveStrategy(self.behavior)

        self.browser_config = BotBrowserConfig()

    def start(self) -> "HumanlikeSeleniumBot":
        if self.driver:
            return self

        try:
            options = self._create_options()
            service = Service(
                self.driver_path,
                log_output=subprocess.STDOUT,
                service_args=["--log", self.driver_log_level],
            )

            width, height = self.browser_config.screen_size
            self.driver = webdriver.Firefox(service=service, options=options)
            self.driver.set_window_size(width, height)
            self._hide_automation_properties()
            return self

        except Exception as e:
            raise Exception(f"브라우저 시작 실패: {e}")

    def _create_options(self) -> Options:
        options = Options()
        options.binary_location = "/Applications/Firefox.app/Contents/MacOS/firefox"
        options.profile = FirefoxProfile(
            "/Users/raynor/Library/Application Support/Firefox/Profiles/udkgggw8.default-release-1732677968237"
        )

        options.set_preference(
            "general.useragent.override",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
        )
        options.set_preference(
            "network.http.accept.default",
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        )
        options.set_preference("network.http.accept-encoding.secure", "gzip, deflate, br")

        options.set_preference("intl.regional_prefs.use_os_locales", True)
        options.set_preference("app.update.enabled", False)
        # 캐시 설정
        options.set_preference("browser.cache.disk.enable", True)
        options.set_preference("browser.cache.memory.enable", True)
        options.set_preference("browser.cache.offline.enable", False)
        options.set_preference("browser.cache.disk.capacity", 1024000)  # 1GB로 제한
        # 브라우저 히스토리 시뮬레이션
        options.set_preference("places.history.enabled", True)
        options.set_preference("browser.formfill.enable", True)
        options.set_preference("signon.rememberSignons", True)
        # 쿠키 설정
        options.set_preference("network.cookie.cookieBehavior", 0)
        options.set_preference("network.cookie.lifetimePolicy", 0)
        # 자동화 탐지 방지
        options.set_preference("dom.webdriver.enabled", False)
        options.set_preference("useAutomationExtension", False)
        options.set_preference("devtools.jsonview.enabled", False)
        options.set_preference("marionette.enabled", False)
        options.set_preference("fission.autostart", False)
        options.set_preference("focusmanager.testmode", False)
        options.set_preference("general.platform.override", "Win32")  # platform 위장
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
        options.set_preference("media.peerconnection.enabled", True)
        options.set_preference("geo.enabled", True)
        # WebGL 설정
        options.set_preference("webgl.disabled", False)
        options.set_preference("webgl.enable-webgl2", True)

        # tor proxy
        if self.use_tor_proxy:
            options.set_preference("network.proxy.type", 1)
            options.set_preference("network.proxy.socks", "127.0.0.1")
            options.set_preference("network.proxy.socks_port", 9050)
            options.set_preference("network.proxy.socks_version", 5)
            options.set_preference("network.proxy.socks_remote_dns", True)
            options.set_preference("network.proxy.http", "")
            options.set_preference("network.proxy.http_port", 0)
            options.set_preference("network.proxy.ssl", "")
            options.set_preference("network.proxy.ssl_port", 0)

        if self.headless:
            options.add_argument("--headless")

        if self.profile_path:
            options.set_preference("profile", self.profile_path)

        return options

    def _hide_automation_properties(self) -> None:
        script = """
        Object.defineProperty(navigator, 'webdriver', {get: () => false});
        Object.defineProperty(navigator, 'automation', {get: () => false});
        """
        self.driver.execute_script(script)
        self.driver.execute_script(
            """
            let script = document.createElement('script');
            script.innerHTML = `
                Object.defineProperty(navigator, 'webdriver', { get: () => false });
                Object.defineProperty(navigator, 'automation', { get: () => false });
            `;
            document.documentElement.prepend(script);
        """
        )

    def _install_addons(self) -> "HumanlikeSeleniumBot":
        raise NotImplementedError()
        self.driver.install_addon("../driver/addons/vpn_master-0.1.4-an+fx.xpi", temporary=False)
        time.sleep(3)

        self.driver.get("about:addons")
        addon_card = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "[data-addon-id*='vpn']"))
        )
        enable_button = addon_card.find_element(By.CSS_SELECTOR, "button[data-l10n-id='enable-addon-button']")
        if enable_button.is_displayed():
            enable_button.click()
            print("VPN 애드온이 활성화되었습니다.")

        return self

    def get(self, url: str) -> "HumanlikeSeleniumBot":
        if not self.driver:
            raise Exception("브라우저가 시작되지 않았습니다. start() 메서드를 먼저 호출하세요.")

        self.driver.get(url)
        self.behavior.random_delay(1, 5)
        return self

    def debug_antibot(self, take_screenshot: bool = True) -> "HumanlikeSeleniumBot":
        self.driver.get("https://bot.sannysoft.com/")
        if take_screenshot:
            self.take_screenshot(f"antibot-{datetime.datetime.now()}.png")
        return self

    def debug_ip(self) -> "HumanlikeSeleniumBot":
        self.get("https://httpbin.org/ip")
        return self

    def debug_detection(self) -> "HumanlikeSeleniumBot":
        detection_script = """
        return {
            webdriver: navigator.webdriver,
            userAgent: navigator.userAgent,
            plugins: navigator.plugins.length,
            languages: navigator.languages,
            platform: navigator.platform,
            automation: window.navigator.webdriver
        };
        """
        result = self.driver.execute_script(detection_script)
        logger.info(result)
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
        self.click_strategy.execute(self.driver, element)
        self.behavior.random_delay(0.5, 2.0)
        return self

    def human_type(
        self,
        element: WebElement,
        text: str,
        clear: bool = True,
    ) -> "HumanlikeSeleniumBot":
        self.type_strategy.execute(self.driver, element, text=text, clear=clear)
        self.behavior.random_delay(0.3, 1.0)
        return self

    def human_scroll(self, direction: str = "down") -> "HumanlikeSeleniumBot":
        self.scroll_strategy.execute(self.driver, element=None, scrolls=random.randint(1, 5), direction=direction)
        return self

    def human_mouse_movement(self) -> "HumanlikeSeleniumBot":
        self.mouse_move_strategy.execute(self.driver, element=None, movements=random.randint(1, 5))
        return self

    def wait_and_click(
        self,
        by: str,
        value: str,
        timeout: int = 10,
    ) -> "HumanlikeSeleniumBot":
        element = self.find_element(by, value, timeout)
        self.human_click(element)
        return self

    def wait_and_type(
        self,
        by: str,
        value: str,
        text: str,
        timeout: int = 10,
        clear: bool = True,
    ) -> "HumanlikeSeleniumBot":
        element = self.find_element(by, value, timeout)
        self.human_type(element, text, clear)
        return self

    def take_screenshot(self, filename: str) -> "HumanlikeSeleniumBot":
        self.driver.save_screenshot(filename)
        return self

    def execute_script(self, script: str, *args) -> "HumanlikeSeleniumBot":
        self.driver.execute_script(script, *args)
        return self

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
