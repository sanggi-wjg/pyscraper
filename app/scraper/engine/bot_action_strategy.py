import logging
import random
import time
from abc import ABC, abstractmethod

from selenium import webdriver
from selenium.common import MoveTargetOutOfBoundsException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.remote.webelement import WebElement

from app.scraper.engine.bot_behavior import HumanBehavior

logger = logging.getLogger(__name__)


class SeleniumBotActionStrategy(ABC):

    def __init__(self, behavior: HumanBehavior):
        self.behavior = behavior

    @abstractmethod
    def execute(self, driver: webdriver.Firefox, element: WebElement | None, **kwargs):
        raise NotImplementedError("act method not implemented")


class HumanClickStrategy(SeleniumBotActionStrategy):

    def execute(self, driver: webdriver.Firefox, element: WebElement | None, **kwargs):
        actions = ActionChains(driver)
        actions.move_to_element(element)
        time.sleep(self.behavior.click_delay())

        x, y = self.behavior.mouse_offset()
        actions.move_by_offset(x, y)

        time.sleep(self.behavior.click_delay())
        actions.click(element)
        actions.perform()


class HumanTypeStrategy(SeleniumBotActionStrategy):

    def execute(self, driver: webdriver.Firefox, element: WebElement | None, **kwargs):
        text = kwargs.get("text")
        clear = kwargs.get("clear", True)

        if not text:
            return

        if clear:
            element.clear()
            self.behavior.random_delay()

        for char in text:
            element.send_keys(char)
            time.sleep(self.behavior.typing_delay())

            if self.behavior.typing_is_failing():
                time.sleep(self.behavior.typing_delay())
                element.send_keys(Keys.BACKSPACE)

                time.sleep(self.behavior.typing_delay())
                element.send_keys(char)


class HumanScrollStrategy(SeleniumBotActionStrategy):

    def execute(self, driver: webdriver.Firefox, element: WebElement | None, **kwargs):
        scrolls = kwargs.get("scrolls", 0)
        direction = kwargs.get("direction", "down")

        if scrolls <= 0:
            return

        for _ in range(scrolls):
            scroll_amount = self.behavior.scroll_amount()
            if direction == "up":
                scroll_amount = -scrolls

            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            self.behavior.random_delay(0.5, 2.0)


class HumanMouseMoveStrategy(SeleniumBotActionStrategy):

    def execute(self, driver: webdriver.Firefox, element: WebElement | None, **kwargs):
        margin = 50
        movements = kwargs.get("movements", 1)

        actions = ActionChains(driver)
        viewport_width = driver.execute_script("return window.innerWidth;")
        viewport_height = driver.execute_script("return window.innerHeight;")

        for _ in range(movements):
            x = max(margin, min(random.randint(-100, 100), viewport_width - margin))
            y = max(margin, min(random.randint(-200, 200), viewport_height - margin))
            try:
                actions.move_by_offset(x, y)
            except MoveTargetOutOfBoundsException as e:
                logger.warning(f"x: {x}, y: {y} / {e.msg}")
                print(f"Failed to move, cause by out of bounds., {e.msg}")
            self.behavior.random_delay(max_time=0.3)

        actions.perform()
