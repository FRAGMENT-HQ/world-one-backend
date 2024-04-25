
FROM python:3.10-alpine



ENV PYTHONUNBUFFERED 1
ENV DJANGO_CONFIGURATION=Prod

RUN mkdir /usr/itb
WORKDIR /usr/itb

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN pip install --upgrade 'sentry-sdk[django]'


COPY . .

CMD ["sh", "-c", "export PYTHONPATH=/usr/itb;export DJANGO_CONFIGURATION=Prod; python manage.py collectstatic --no-input;python manage.py makemigrations;python manage.py migrate;gunicorn Backend.wsgi:application -b 0.0.0.0:9006 --timeout 60000 "]