FROM python:3.12-bullseye as django

RUN apt-get update && apt-get install --no-install-recommends -y \
  dumb-init \
  build-essential \
  python3-setuptools \
  python3-dev \
  libpq-dev\
 && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
