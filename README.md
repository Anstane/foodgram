# Foodgram

Контейнеризированное приложение для публикации своих рецептов в виде социальной сети с возможностью постить фотографии, описание, оформлять теги, подписываться на авторов и формировать список продукотов для покупок.

Было написано backend приложение с API по заданному техническому заданию и упаковано в Docker-контейнеры.

Использованный стек технологий: Django 2.2.16 | DRF 3.12.4 | Gunicorn 20.0.4
Бибилиотеки: Djoser | Pillow | python-dotenv


## Установка приложения

#### 1. Устанавливаем Docker

```
  https://www.docker.com/
```

#### 2. Клонируем репозиторий

```
  git@github.com:Anstane/foodgram-project-react.git
```

#### 3. Запускаем Docker compose

```
  -Для установки из репозитория:

  docker compose -f docker-compose.local.yml up

  -Для установки с DockerHub:

  docker compose up
```

#### 4. Делаем миграции

```
  docker compose exec backend python manage.py makemigrations
  docker compose exec backend python manage.py migrate
```

#### 5. Собираем статику для backend`а

```
  docker compose exec backend python manage.py collectstatic
  docker compose exec backend cp -r ../app/static_backend/. ../var/html/
```

#### Пользуемся приложением.

## Документация проекта

`/api/docs/`

## Автор

- [@Anstane](https://github.com/Anstane)

