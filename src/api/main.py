import argparse
import uvicorn
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI


from model import LLMModel
from db_client import MarqoClient

app = FastAPI()

marqo_client = MarqoClient()
llm_model = LLMModel(temperature=float(os.getenv("MODEL_TEMPERATURE")), max_tokens=8000)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/db/health")
def db_health():
    return marqo_client.health()


@app.post("/ask")
def ask(question: str):
    results = marqo_client.search(question)
    context = ""
    for i, hit in enumerate(results["hits"]):
        title = hit["title"]
        text = hit["text"]
        context += f"Source {i}) {title} || {" ".join(text.split())}... \n"
    response = llm_model.ask_question(question, context)
    return response["choices"][0]["text"]


@app.get("/")
def read_root():
    return {"message": "Welcome to LLama LLM API!"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the FastAPI application.")
    parser.add_argument(
        "--host",
        type=str,
        default=os.getenv("API_HOST", "0.0.0.0"),
    )
    args = parser.parse_args()
    uvicorn.run(app, host=args.host, port=5000)
