import argparse
import uvicorn

from fastapi import FastAPI

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scraping import Fetcher

app = FastAPI()

fetcher = Fetcher()


@app.get("/")
def read_root():
    return {"message": "Welcome to Scraping microservice!"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/db/health")
def db_health():
    return fetcher.client.health()


@app.post("/fetch_hotmart_info")
def store_hotmart_info(url: str):
    infos = fetcher.fetch_info_from(url)
    fetcher.client.store_infos_to_index(infos, index_name="web-content")
    return "ok", 201


@app.post("/db/store_info_to_index")
def store_to_db(text: str, index_name: str):
    fetcher.client.store_info_to_index(text, index_name)
    return "ok", 201


@app.post("/db/fetch_from_url")
def fetch_from_url(url: str):
    fetcher.client.store_info_from_url(url)
    return "ok", 201


@app.delete("/db/indexes")
def clear_indexes():
    fetcher.client.clear_all_indexes()
    return "ok", 204


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the FastAPI application.")
    parser.add_argument(
        "--host",
        type=str,
        default=os.getenv("API_HOST", "0.0.0.0"),
    )
    args = parser.parse_args()
    uvicorn.run(app, host=args.host, port=5001)
