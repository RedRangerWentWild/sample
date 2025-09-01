import requests
from bs4 import BeautifulSoup
import logging
from typing import Dict, Optional

# Configure logging for professional touch
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

class BookScraper:
    def __init__(self, url: str):
        self.url = url
        self.soup: Optional[BeautifulSoup] = None

    def fetch_page(self) -> None:
        """Fetches the webpage and parses it into BeautifulSoup."""
        logging.info(f"Fetching data from {self.url} ...")
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.text, "html.parser")
            logging.info("Page fetched successfully ✅")
        except requests.RequestException as e:
            logging.error(f"Failed to fetch page: {e}")
            raise

    def scrape_book_info(self) -> Dict[str, str]:
        """Extracts book information from the infobox if available."""
        if not self.soup:
            raise ValueError("Soup object is empty. Did you run fetch_page()?")

        infobox = self.soup.find("table", class_="infobox")
        book_data: Dict[str, str] = {}

        if not infobox:
            logging.warning("No infobox found on the page.")
            return book_data

        for row in infobox.find_all("tr"):
            header = row.find("th")
            cell = row.find("td")
            if header and cell:
                key = header.get_text(" ", strip=True)
                val = cell.get_text(" ", strip=True)
                book_data[key] = val

        return book_data

    def pretty_print(self, data: Dict[str, str]) -> None:
        if not data:
            print("No book data available to display.")
            return
        print("\n📖 Scraped Book Information:")
        print("-" * 40)
        for k, v in data.items():
            print(f"{k:15}: {v}")


if __name__ == "__main__":
    # Example Wikipedia page for a book
    url = "http://httpbin.org/get"
    scraper = BookScraper(url)

    scraper.fetch_page()
    book_info = scraper.scrape_book_info()
    scraper.pretty_print(book_info)
