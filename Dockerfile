FROM python:3.12-alpine3.20

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    make

COPY ./requirements.pip ./requirements.pip
RUN pip install --upgrade pip && \
    pip install -r requirements.pip

COPY ./run.py ./run.py
COPY ./entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]