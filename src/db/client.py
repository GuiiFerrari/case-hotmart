import logging
import marqo
import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_PATH, ".."))
sys.path.append(os.path.join(BASE_PATH, "..", ".."))

from fetchers import fetch_info_from

HOST = "http://localhost"
PORT = "8882"
LOGGER = logging.getLogger(__name__)


class MarqoClient:

    def __init__(self):
        self.client = marqo.Client(f"{HOST}:{PORT}")

    def health(self):
        return self.client.http.get("/health")

    def store_info_from_url(self, url: str, index_name: str = "web-content"):
        try:
            self.client.create_index(index_name)
        except Exception:
            pass
        infos: list[dict] = fetch_info_from(url)
        self.client.index(index_name).add_documents(infos, tensor_fields=["text"])
        LOGGER.info(f"Stored infos from {url} in index {index_name}")

    def search(self, query: str, index_name: str = "web-content"):
        search_results = self.client.index(index_name).search(
            query, searchable_attributes=["text"], search_method="TENSOR"
        )
        return search_results

    def clear_index(self, index_name: str = "web-content"):
        try:
            self.client.index(index_name).clear()
        except Exception:
            pass
        LOGGER.info(f"Cleared index {index_name}")

    def clear_all_indexes(self):
        for index in self.client.list_indexes():
            self.client.index(index).clear()
        LOGGER.info("Cleared all indexes")
