FROM python:3.6

LABEL mantainer="ricardoleoncorreia"

ENV HTTP_PROXY 'http://e10206:rick.007@10.162.64.36:8080'
ENV HTTPS_PROXY 'http://e10206:rick.007@10.162.64.36:8080'

# Install required packages and remove the apt packages cache when done.
COPY uwsgi/apt.conf /etc/apt/apt.conf
RUN apt-get update && \
    apt-get upgrade -y && \ 	
    apt-get install -y \
	build-essential \
	libssl-dev \
	libffi-dev \
	# libmysqlclient-dev \
	nginx \
	supervisor

COPY . /root/

RUN pip install --upgrade pip && \
    pip --no-cache-dir install \
    -r /root/uwsgi/requirements.txt

EXPOSE 8000
WORKDIR /root/api/
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
# CMD [ "ls", "-al" ]
# CMD [ "pip", "freeze" ]