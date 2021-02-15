FROM python:3-alpine
MAINTAINER Jake Sloan <jsloan@red-button.com> 
RUN apk update && apk upgrade && pip install -U pip
RUN apk add --update alpine-sdk bash make gcc libxslt-dev libxml2-dev libc-dev openssl-dev libffi-dev zlib-dev openssh mysql-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev\
    && rm -rf /var/cache/apk/*
	
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
# Expose the Flask port
EXPOSE 5000
ENV PYTHONPATH="/opt/python:${PYTHONPATH}"
CMD [ "python3", "/opt/www/site.py" ]
