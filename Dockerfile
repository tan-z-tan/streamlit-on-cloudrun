FROM python:3.9-slim
EXPOSE 8080

RUN apt-get update \
    && apt-get install --no-install-recommends -y build-essential \
    && pip install poetry \ 
    && poetry config virtualenvs.create false

WORKDIR /app
COPY app ./app
COPY model_files ./model_files
COPY samples ./samples
COPY pyproject.toml .
COPY poetry.lock .
COPY app.py .

RUN poetry install

CMD poetry run streamlit run app.py --server.port 8080
