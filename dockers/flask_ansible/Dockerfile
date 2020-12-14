
FROM python:3.8-alpine
COPY flask/app.py /flask/
RUN mkdir /root/.ansible
RUN mkdir /root/.ansible/plugins
RUN mkdir /root/.ansible/plugins/modules
COPY ansible/models/ocnos/ocnos_config.py /root/.ansible/plugins/modules/
run apk update && apk upgrade


RUN apk add --no-cache \
      bash \
      build-base \
      ca-certificates \
      cyrus-sasl-dev \
      graphviz \
      jpeg-dev \
      libevent-dev \
      libffi-dev \
      libxslt-dev \
      openldap-dev \
      postgresql-dev
	  
run apk add gcc

RUN pip3 install ansible 

RUN pip3 install flask
RUN pip3 list
RUN apk add nano


CMD ["python3","/flask/app.py"]


