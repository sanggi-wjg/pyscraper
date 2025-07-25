import httpx
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def get_user_agent():
    """Returns a random User-Agent string."""
    ua = UserAgent()
    return ua.random


def scrape_product(url: str):
    """Scrapes product information from a given URL."""
    headers = {"User-Agent": get_user_agent()}
    try:
        with httpx.Client() as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for bad status codes

        soup = BeautifulSoup(response.text, "html.parser")

        # NOTE: These are placeholders. Selectors need to be adjusted for the actual website.
        product_name = soup.select_one("#productName").text.strip()
        price_str = (
            soup.select_one("#price").text.strip().replace("₩", "").replace(",", "")
        )
        product_price = float(price_str)
        platform = "ExampleShop"  # Placeholder

        return {
            "name": product_name,
            "price": product_price,
            "platform": platform,
            "url": url,
            "discount": "",  # Placeholder for discount info
        }

    except httpx.RequestError as e:
        print(f"Error during request to {url}: {e}")
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
    return None
