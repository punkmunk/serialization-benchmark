FROM python:3.11-slim

COPY proxy/requirements.txt .
RUN pip install -r requirements.txt

COPY proxy proxy
COPY config.json config.json

ENV CONFIG=config.json

ENTRYPOINT ["python", "proxy/proxy.py"]
