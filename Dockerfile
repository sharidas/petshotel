FROM ubuntu:20.04

RUN apt-get update

RUN apt-get install -y python3 python3-virtualenv mongodb

WORKDIR /usr/src/app

ENV VIRTUALENV /opt/env
RUN virtualenv --python python3 ${VIRTUALENV}

ENV PATH="${VIRTUALENV}/bin:$PATH"

COPY ./requirements.txt /usr/src/app

RUN pip install --upgrade pip
RUN pip install --use-feature=2020-resolver -r requirements.txt

COPY . /usr/src/app

ENV FLASK_APP /usr/src/app/wsgi.py
ENV FLASK_ENV production

ENTRYPOINT /etc/init.d/mongodb start && FLASK_APP=wsgi.py FLASK_ENV="production" flask run --host=0.0.0.0


