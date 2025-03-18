import logging
from src.scraping.db_client import MarqoClient

LOGGER = logging.getLogger(__name__)

# https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF/blob/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf


def run_process():
    client = MarqoClient()
    # client.clear_index()
    # client.store_info_from_url("https://hotmart.com/pt-br/blog/como-funciona-hotmart")
    results = client.search("hotmart")
    for hit in results["hits"]:
        print(f"Question: {hit['question']}")
        print(f"Snippet: {hit['text'][:300]}...\n")
    print()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_process()
