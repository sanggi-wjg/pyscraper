import random
import time
from abc import ABC, abstractmethod
from typing import Tuple


class SeleniumBotBehavior(ABC):

    @abstractmethod
    def random_delay(self, min_time: float, max_time: float):
        raise NotImplementedError()

    @abstractmethod
    def typing_delay(self) -> float:
        raise NotImplementedError()

    @abstractmethod
    def click_delay(self) -> float:
        raise NotImplementedError()

    @abstractmethod
    def scroll_amount(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def mouse_offset(self) -> Tuple[int, int]:
        raise NotImplementedError()


class HumanBehavior(SeleniumBotBehavior):

    def __init__(self, speed_factor: float = 1.0):
        self.speed_factor = speed_factor
        self.typing_fail_probability = 0.1

    def random_delay(self, min_time: float = 0.1, max_time: float = 2.0):
        delay = random.uniform(min_time, max_time)
        time.sleep(delay)

    def typing_is_failing(self):
        return random.random() < self.typing_fail_probability

    def typing_delay(self) -> float:
        return random.uniform(0.05, 0.2) / self.speed_factor

    def click_delay(self) -> float:
        return random.uniform(0.1, 0.3) / self.speed_factor

    def scroll_amount(self) -> int:
        return random.randint(200, 800)

    def mouse_offset(self) -> Tuple[int, int]:
        return random.randint(-3, 3), random.randint(-3, 3)
