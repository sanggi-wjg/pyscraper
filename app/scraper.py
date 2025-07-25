import httpx
from bs4 import BeautifulSoup

from app.util.util_user_agent import get_fake_headers


class AboutPetScraper:

    # def __init__(self):
    #     super().__init__()
    #     self.handler = HttpHandler()

    def scrape(self, url: str):
        try:
            headers = get_fake_headers()
            headers["Accept"] = (
                "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
            )
            headers["Accept-Language"] = "ko,en-US;q=0.9,en;q=0.8"

            with httpx.Client() as client:
                response = client.get(url, headers=get_fake_headers())
                response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            for item in soup.select(".gd-item"):
                link = item.select_one("a")["href"]
                discount = item.select_one(".disc").text.strip()
                name = item.select_one(".tit").text.strip()
                price = item.select_one(".price em").text.strip()
                print(f"Product: {name}, Price: {price}, Discount: {discount}, Link: {link}")

        except httpx.RequestError as e:
            return None
