import logging
import random
from typing import Optional

import httpx

logger = logging.getLogger(__name__)

# https://free-proxy-list.net/ko/anonymous-proxy.html
_CANDIDATE_PROXIES = [
    "http://57.129.81.201:8080",
    "http://103.127.252.57:3128",
    "http://8.219.97.248:80",
]
random.shuffle(_CANDIDATE_PROXIES)


def test_proxy_connection(
    proxy_url: str,
    test_url: str = "https://httpbin.org/ip",
) -> bool:
    with httpx.Client(proxies=proxy_url, timeout=10) as client:
        try:
            response = client.get(test_url)
            response.raise_for_status()
            logger.debug(f"✅ Proxy connected. IP: {response.text}")
            return True

        except httpx.RequestError as e:
            logger.debug(f"❌ Proxy connection failed. Proxy: {proxy_url}")
            logger.debug(e)
            return False


def get_working_proxy() -> Optional[str]:
    logger.info("🔍 Searching for a working proxy...")

    for proxy in _CANDIDATE_PROXIES:
        if test_proxy_connection(proxy):
            logger.info(f"✅ Using working proxy: {proxy}")
            return proxy

    logger.error("❌ No working proxy found.")
    return None
