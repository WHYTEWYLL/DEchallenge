FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

RUN python3 advance/main.py --adhoc true
