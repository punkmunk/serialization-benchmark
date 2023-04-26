FROM python:3.11-slim

COPY bench/requirements.txt .
RUN pip install -r requirements.txt

COPY bench bench
COPY config.json config.json

ENV CONFIG=config.json

ENTRYPOINT ["python", "bench/bench.py"]
