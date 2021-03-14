FROM python:3.6-alpine
ADD . /code
WORKDIR /code
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps && \
 pip install -r requirements.txt

CMD ["python", "api.py"]
# ENTRYPOINT gunicorn --workers=4 --bind=0.0.0.0:5000 --access-logfile=- api:app
