FROM python:3.13-slim

RUN groupadd --gid 10001 appgroup \
    && useradd \
        --uid 10001 \
        --gid 10001 \
        --no-create-home \
        --shell /bin/bash \
        appuser

RUN apt update &&  apt install xvfb -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN python -m venv venv

ENV PATH="/app/venv/bin:$PATH"

RUN pip install -r requirements.txt

USER appuser

CMD ["xvfb-run","-a","python", "main.py"]