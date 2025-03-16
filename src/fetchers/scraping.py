import logging
import requests

from bs4 import BeautifulSoup

LOGGER = logging.getLogger(__name__)


def fetch_info_from(url: str) -> list[dict[str, str]]:
    """
    Fetches information from a given URL.

    Args:
        url (str): URL to fetch information from.

    Returns:
        list[dict[str, str]]: List of dictionaries containing
            the question title and text of the fetched content.
    """
    LOGGER.info(f"Fetching info from {url}")
    response = requests.get(url)
    LOGGER.info(f"Response status code: {response.status_code}")
    soup = BeautifulSoup(response.text, "html.parser")
    content: list[dict[str, str]] = []
    for h2 in soup.find_all("h2"):
        next_node = h2.find_next_sibling()
        text = []
        while next_node and next_node.name != "h2":
            if next_node.name == "p":
                text.append(next_node.get_text())
            next_node = next_node.find_next_sibling()
        content.append({"question": h2.get_text(), "text": " ".join(text)})
    return content


if __name__ == "__main__":
    fetch_info_from("https://hotmart.com/pt-br/blog/como-funciona-hotmart")
