FROM python:3.8.6-slim-buster

ENV APPDIR=/app/pdfparse \
    PYTHONPATH=/app \
    PYTHONBUFFERED=1
RUN mkdir -p $APPDIR
WORKDIR $APPDIR

COPY . .
RUN pip install --no-cache-dir --editable .

RUN mkdir /app/data/
