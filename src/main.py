from fastapi import FastAPI

import uvicorn

from model import LLMModel
from db.client import MarqoClient
from fetchers.scraping import fetch_info_from

app = FastAPI()

marqo_client = MarqoClient()
llm_model = LLMModel(temperature=0.5, max_tokens=8000)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/db/health")
def db_health():
    return marqo_client.health()


@app.post("/db/fetch_from_url")
def fetch_from_url(url: str):
    marqo_client.store_info_from_url(url)
    return "ok", 201


@app.delete("/db/indexes")
def clear_indexes():
    marqo_client.clear_all_indexes()
    return "ok", 204


@app.post("/ask")
def ask(question: str):
    results = marqo_client.search(question)
    context = ""
    for i, hit in enumerate(results["hits"]):
        title = hit["question"]
        text = hit["text"]
        context += f"Source {i}) {title} || {" ".join(text.split())}... \n"
    response = llm_model.ask_question(question, context)
    return response["choices"][0]["text"]


@app.get("/")
def read_root():
    return {"message": "Welcome to LLama LLM API!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
