FROM python:3.5.2-alpine
MAINTAINER Ivan Pedrazas <ipedrazas@gmail.com>


RUN pip install  \
    flask


COPY . /src
WORKDIR /src

CMD ["python", "./app.py"]

