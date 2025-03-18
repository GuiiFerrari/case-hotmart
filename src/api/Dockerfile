FROM python:3.12-bullseye

WORKDIR /app

RUN mkdir models && curl -LJ -o models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY main.py model.py db_client.py ./

EXPOSE 5000


# CMD ["sleep", "600"]

CMD ["python", "main.py", "--host", "0.0.0.0"]
