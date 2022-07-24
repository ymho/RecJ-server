#FROM ubuntu:latest
#USER root
#
#RUN apt-get update
#RUN apt-get install python3 python3-pip -y
#RUN apt-get install -y nano less
#
#RUN pip install dateutil
#
#RUN pip3 install flask
#RUN pip install folium dateutil
#
#RUN mkdir /app
#


FROM python:3.8

RUN apt update

RUN apt install -y nano less
RUN pip install --upgrade pip
RUN pip install setuptools==57.4.0

ADD ./app/ /app/
RUN cd /app && mkdir csv
RUN cd /app && mkdir results


RUN pip install flask folium python-dateutil python-csv numpy
