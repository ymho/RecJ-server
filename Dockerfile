FROM python:3.8
USER root

RUN apt-get update

RUN apt-get install -y nano less
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

RUN pip install flask
COPY app.py /root/app.py
