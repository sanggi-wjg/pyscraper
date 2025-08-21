import logging
from urllib.parse import urlparse

from selenium.common import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

logger = logging.getLogger(__name__)


def safe_extract_text(element, selector: str) -> str:
    try:
        found = element.select_one(selector)
        return found.get_text(strip=True) if found else ""
    except (AttributeError, TypeError):
        return ""


def safe_extract_attr(element, selector: str, attr: str) -> str:
    try:
        found = element.select_one(selector)
        return found.get(attr, "") if found else ""
    except (AttributeError, TypeError):
        return ""


def safe_extract_text_by_bot(element: WebElement, by: str, selector: str) -> str:
    try:
        return element.find_element(by, selector).text
    except (AttributeError, TypeError):
        return ""
    except NoSuchElementException as e:
        logger.warning(f"No such selector in element, {e}")
        return ""


def safe_extract_attr_by_bot(element: WebElement, by: str, selector: str, attr: str) -> str:
    try:
        return element.find_element(by, selector).get_attribute(attr)
    except (AttributeError, TypeError):
        return ""
    except NoSuchElementException as e:
        logger.warning(f"No such attr in element, {e}")
        return ""


def clean_url(url: str) -> str:
    try:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    except:
        logger.warning(f"Failed to clean url, {url}")
        return url
