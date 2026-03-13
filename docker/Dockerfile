FROM python:3.13

# Wait for args
ARG DJANGO_ENV

# Tell python to show in console both standards: out & error
ENV PYTHONUNBUFFERED=1
ENV HTTP_PROXY http://E10356:Jcbb-2390-2024@10.162.64.36:8080
ENV HTTPS_PROXY http://E10356:Jcbb-2390-2024@10.162.64.36:8080

# Proxy set up
COPY apt.conf /etc/apt/apt.conf
COPY gunicorn_conf.py /backend/conf/gunicorn_conf.py

# Fix missing packages, install uwsgi
#RUN apt-get update --fix-missing && \
#    apt-get install -y build-essential libssl-dev libffi-dev

# Copy requirements to root folder
COPY requirements/base.txt /root/
COPY requirements/base.txt /root/
COPY jupyter_notebook_config.py /root/.jupyter/jupyter_notebook_config.py

# 1. Upgrade pip
# 2. Install (skip cache) requirements
RUN pip install --upgrade pip && \
    pip --no-cache-dir install \
    -r /root/base.txt