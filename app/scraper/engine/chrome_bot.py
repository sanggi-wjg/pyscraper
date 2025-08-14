# import logging
# import subprocess
#
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from selenium_stealth import stealth
#
# from app.scraper.engine.bot import HumanlikeSeleniumBot
#
# logger = logging.getLogger(__name__)
#
#
# class HumanlikeChromeSeleniumBot(HumanlikeSeleniumBot):
#
#     def __init__(
#         self,
#         driver_path: str = "../driver/chromedriver",
#         driver_log_level: str = "info",
#         use_tor_proxy: bool = False,
#         headless: bool = False,
#         speed_factor: float = 1.0,
#         profile_path: str | None = None,
#     ):
#         super().__init__(driver_path, driver_log_level, use_tor_proxy, headless, speed_factor, profile_path)
#
#     def start(self) -> "HumanlikeSeleniumBot":
#         if self.driver:
#             return self
#
#         try:
#             options = self._create_options()
#             service = Service(
#                 self.driver_path,
#                 log_output=subprocess.STDOUT,
#                 service_args=["--log", self.driver_log_level],
#             )
#
#             width, height = self.browser_config.screen_size
#             self.driver = webdriver.Chrome(service=service, options=options)
#             self.driver.set_window_size(width, height)
#             self._hide_automation_properties()
#             # selenium-stealth
#             stealth(
#                 self.driver,
#                 languages=["en-US", "en"],
#                 vendor="Google Inc.",
#                 platform="Win32",
#                 webgl_vendor="Intel Inc.",
#                 renderer="Intel Iris OpenGL Engine",
#                 fix_hairline=True,
#             )
#             return self
#
#         except Exception as e:
#             raise Exception(f"브라우저 시작 실패: {e}")
#
#     def _create_options(self) -> Options:
#         options = Options()
#         # 1. 자동화 탐지 방지
#         options.add_argument("--disable-blink-features=AutomationControlled")
#         options.add_argument("--disable-blink-features=block-new-window")
#         options.add_experimental_option("excludeSwitches", ["enable-automation"])
#         options.add_experimental_option("useAutomationExtension", False)
#
#         # 2. 브라우저 창 설정
#         options.add_argument("--start-maximized")  # 전체화면
#         # options.add_argument("--headless=new")  # 헤드리스 모드 (탐지 위험 ↑)
#
#         # 3. 개인정보 보호 및 보안 우회
#         options.add_argument("--disable-infobars")
#         options.add_argument("--disable-extensions")
#         options.add_argument("--disable-plugins")
#         options.add_argument("--disable-images")  # 이미지 로딩 비활성화 (속도 향상)
#         options.add_argument("--disable-javascript")  # JS 비활성화 (주의: 일부 사이트는 필요)
#         options.add_argument("--no-sandbox")
#         options.add_argument("--disable-dev-shm-usage")
#         options.add_argument("--disable-gpu")
#         options.add_argument("--remote-debugging-port=9222")
#
#         # 4. 사용자 에이전트 (User-Agent) 설정 (랜덤 추천)
#         options.add_argument(
#             "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
#         )
#
#         # 5. 언어 및 위치 설정
#         options.add_argument("--lang=ko-KR")
#         options.add_argument("--accept-lang=ko-KR")
#
#         # 6. 웹RTC IP 우회 (로컬 IP 숨기기)
#         options.add_argument("--disable-webrtc")
#         options.add_argument("--disable-features=WebRtcHideLocalIpsWithMdns")
#
#         # 7. 프록시 사용 (선택적)
#         # options.add_argument("--proxy-server=socks5://127.0.0.1:9050")  # Tor
#         # options.add_argument("--proxy-server=http://user:pass@proxy-server:port")
#
#         # 8. 쿠키/세션 분리 (각 실행마다 새 프로필)
#         options.add_argument("--user-data-dir=/path/to/custom/profile")  # 커스텀 프로필
#         options.add_argument("--profile-directory=Default")
#         return options
#
#     def _hide_automation_properties(self) -> None:
#         self.driver.execute_cdp_cmd(
#             "Page.addScriptToEvaluateOnNewDocument",
#             {
#                 "source": """
#         Object.defineProperty(navigator, 'webdriver', {
#             get: () => false,
#         });
#         Object.defineProperty(navigator, 'languages', {
#             get: () => ['ko-KR', 'ko', 'en-US', 'en'],
#         });
#         Object.defineProperty(navigator, 'plugins', {
#             get: () => [1, 2, 3, 4, 5],
#         });
#         Object.defineProperty(navigator, 'platform', {
#             get: () => 'Win32',
#         });
#         window.chrome = {
#             runtime: {},
#             loadTimes: () => {},
#             csi: () => {}
#         };
#         Object.defineProperty(navigator, 'chrome', {
#             get: () => window.chrome
#         });
#         // permissions 흉내
#         const originalQuery = window.navigator.permissions.query;
#         window.navigator.permissions.query = (parameters) => (
#             parameters.name === 'notifications' ?
#                 Promise.resolve({ state: 'denied' }) :
#                 originalQuery(parameters)
#         );
#     """
#             },
#         )
