# Dagster libraries to run both dagster-webserver and the dagster-daemon. Does not
# need to have access to any pipeline code.

FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    python3-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip install --no-cache-dir \
    dagster-postgres \
    dagster \
    dagit \
    httpx \
    pandas \
    sqlalchemy

RUN mkdir -p /opt/dagster/dagster_home /opt/dagster/app

ENV DAGSTER_HOME=/opt/dagster/dagster_home

ENV PYTHONPATH="/opt/dagster/app:${PYTHONPATH}"

COPY dagster.yaml /opt/dagster/dagster_home/dagster.yaml

COPY . /opt/dagster/app

EXPOSE 3000

WORKDIR /opt/dagster/app

CMD ["dagster-webserver", "-f", "etl.py", "-h", "0.0.0.0", "-p", "3000"]


