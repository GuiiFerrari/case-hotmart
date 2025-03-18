FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY main.py scraping.py db_client.py ./

EXPOSE 5001

CMD ["python", "main.py", "--host", "0.0.0.0"]
