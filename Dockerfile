FROM python:3.5.2-alpine
MAINTAINER Ivan Pedrazas <ipedrazas@gmail.com>


RUN pip install  \
    flask requests requests-futures

LABEL description="Mocking services based on a json file or a json schema."
LABEL base="alpine"
LABEL language="python"

COPY . /src
WORKDIR /src

CMD ["python", "./app.py"]
