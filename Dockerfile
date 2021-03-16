FROM python:3.6-alpine

WORKDIR /code

COPY requirements.txt /code

RUN apk update --no-cache \
&& apk add build-base postgresql-dev libpq --no-cache --virtual .build-deps \
&& pip install --no-cache-dir --upgrade pip \
&& pip install --no-cache-dir -r requirements.txt \
&& apk del .build-deps
RUN apk add postgresql-libs libpq --no-cache

ADD . /code

RUN python3 -m pip install -r requirements.txt --user

CMD ["python", "api.py"]
# ENTRYPOINT gunicorn --workers=4 --bind=0.0.0.0:5000 --access-logfile=- api:app
