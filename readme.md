# SScrapper Project

Aplicación para alertar sobre ofertas de productos

## Instalación

Para instalar y ejecutar la aplicación se debe tener instalad docker y docker-compose

Link Docker:
https://www.digitalocean.com/community/tutorials/como-instalar-y-usar-docker-en-ubuntu-18-04-1-es

Link Docker-Compose: https://docs.docker.com/compose/install/

## Deploy

```bash

docker build -t scrapper:latest .
docker-compose up

docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

```

## Urls

Url Admin: 127.0.0.1:8000/admin

Url Principal: 127.0.0.1:8000
