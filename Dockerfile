FROM python:3.6.9-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /uitests
WORKDIR /uitests
COPY requirements.txt /uitests/
RUN pip install -r requirements.txt
COPY . /uitests/
CMD pytest
