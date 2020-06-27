# Docker app with Django and Scrapyd as service
indow_backend is crawler based app backend

3# 1- Download docker app for Windows or mac
https://docs.docker.com/get-docker/

## 2- Make `Dockerfile` and `docker-compose.yml` file using this documentation
https://docs.docker.com/compose/django/


## 3- run the app
> docker-compose up

## 4- migrate schema
> docker-compose run django bash -c "python manage.py migrate && python manage.py createsuperuser"
