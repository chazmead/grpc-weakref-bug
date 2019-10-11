FROM python:3.7-alpine3.10

RUN apk update && apk --no-cache add libxml2-dev python3-dev libxslt-dev g++ py3-pip
COPY ./requirements.txt /app/requirements.txt
RUN ["pip", "install", "-r", "/app/requirements.txt"]

COPY ./src /app/src
WORKDIR /app/src
CMD ["python", "main.py"]
