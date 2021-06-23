FROM docker.io/python:3.9

RUN mkdir /app

WORKDIR /app

RUN pip install urllib3

COPY bitcoin_service.py /app/

ENTRYPOINT ["/usr/local/bin/python", "/app/bitcoin_service.py"]
