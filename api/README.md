# Код FastAPI-приложения

## Локальный запуск
Для запуска api локально необходимо создать файл `core/.env` со следующими параметрами:

- SERVICE_HOST - хост сервиса
- SERVICE_PORT - порт сервиса
- SERVICE_SECRET_KEY - секретный ключ для проверки JWT (должен совпадать с ключом сервиса авторизации)
- MONGO_HOST - хост MongoDB
- MONGO_PORT - порт MongoDB
- MONGO_DB - БД MongoDB
- MONGO_LIKES - название коллекции лайков фильмов
- MONGO_BOOKMARKS - название коллекции закладок фильмов
- MONGO_REVIEWS - название коллекции рецензий на фильмы
- MONGO_REVIEWS_LIKES - название коллекции лайков к рецензиям


## Запуск в docker
Для запуска api через docker compose необходимо создать файл `core/docker.env` с теми же параметрами
