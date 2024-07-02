FROM python:3.12.4-alpine3.19

RUN apk update && \
    apk add --no-cache \
        build-base \
        postgresql-dev \
        libpq

RUN mkdir /profiler
WORKDIR /profiler

COPY requirements.txt /profiler/
RUN pip install --no-cache-dir -r /profiler/requirements.txt

COPY run.py /profiler/
COPY profilerApp /profiler/profilerApp

ENV FLASK_APP=run.py
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
