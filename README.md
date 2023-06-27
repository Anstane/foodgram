# Foodgram

Контейнеризированное приложение для публикации своих рецептов.

URL: https://foodgramproject.sytes.net/

Admin User: Anstyk@yandex.ru

Password: 5WfwS3


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
## Author

- [@Anstane](https://github.com/Anstane)

