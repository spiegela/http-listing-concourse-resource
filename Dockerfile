FROM python:3

WORKDIR /usr/src/app
ADD assets/ /opt/resource/
RUN pip install --no-cache-dir -r /opt/resource/requirements.txt
RUN chmod +x /opt/resource/*
