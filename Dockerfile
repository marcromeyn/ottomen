FROM orchardup/python:2.7
ADD . /code
WORKDIR /code
RUN apt-get update && apt-get install -y \
    build-essential \
    python-psycopg2 \
    python-numpy \
    python-scipy \
    python-gevent \
    git \
    curl

ADD requirements.txt /src/requirements.txt
RUN cd /src && pip install -r requirements.txt && cd ../
RUN pip install -U pytest

RUN curl --silent --location https://deb.nodesource.com/setup_0.12 | sudo bash - && sudo apt-get install --yes nodejs
RUN npm install -g gulp
RUN npm install -g browser-sync
ADD package.json /src/package.json
RUN cd /src && npm install