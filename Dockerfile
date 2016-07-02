FROM python:3.5

RUN mkdir -p /usr/src/app
COPY . /usr/src/app
RUN pip install --no-cache-dir -e /usr/src/app

ENTRYPOINT ["prime"]
