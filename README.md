# Docker app with Django and Scrapyd as service
indow_backend is crawler based app backend

### 1- Download docker app for Windows or mac
https://docs.docker.com/get-docker/

### 2- Make `Dockerfile` and `docker-compose.yml` file using this documentation
https://docs.docker.com/compose/django/

### 3- Update DB credentails in `local_settings` file and crawler `settings` file

### 4- Update container/local machine IP Address in project `settings` file's `SCRAPYD_SERVER_URL` variable

### 5- migrate schema
> docker-compose run django bash -c "python manage.py migrate && python manage.py createsuperuser"

### 6- run the app
> docker-compose up
