FROM python:3.5.2-alpine
MAINTAINER Ivan Pedrazas <ipedrazas@gmail.com>

RUN apk add --update bash curl && \
    rm -rf /var/cache/apk/*

RUN pip install  \
    flask requests requests-futures redis

LABEL description="Mocking services based on a json file or a json schema."
LABEL base="alpine"
LABEL language="python"

COPY . /src
WORKDIR /src

CMD ["python", "./app.py"]
