import logging
import os

from marqo.client import Client
from marqo.index import Index

HOST = "http://" + os.getenv("MARQO_HOST", "localhost")
PORT = os.getenv("MARQO_PORT", "8882")
LOGGER = logging.getLogger(__name__)


class MarqoClient:

    def __init__(self):
        self.client = Client(f"{HOST}:{PORT}")

    def health(self):
        return self.client.http.get("/health")

    def store_infos_to_index(
        self,
        infos: list[dict[str, str]],
        index_name: str,
        tensor_fields: list[str] = ["text"],
    ):
        try:
            self.client.create_index(index_name)
        except Exception:
            pass
        tensor_fields = ["text"]
        index: Index = self.client.index(index_name)
        res = index.add_documents(infos, tensor_fields=tensor_fields)
        LOGGER.info(f"Stored infos in index {index_name}")

    def search(
        self,
        query: str,
        index_name: str = "web-content",
    ):
        index: Index = self.client.index(index_name)
        search_results = index.search(
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
