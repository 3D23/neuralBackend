FROM python:3.11-slim as cache

WORKDIR /app
COPY requirements.txt .

RUN pip install --upgrade pip && \
    mkdir /pip_cache && \
    pip install --cache-dir /pip_cache -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

COPY --from=cache /pip_cache /pip_cache
COPY --from=cache /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=cache /usr/local/bin/uvicorn /usr/local/bin/uvicorn
COPY . .

RUN pip install --no-index --find-links=/pip_cache -r requirements.txt

EXPOSE 8023
CMD ["/usr/local/bin/uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8023"]