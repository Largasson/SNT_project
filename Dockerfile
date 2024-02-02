FROM python:3.11.7-slim

ENV FLASK_APP=web_app.app
ENV FLASK_ENV=development


RUN python -m pip install --upgrade pip

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . .
