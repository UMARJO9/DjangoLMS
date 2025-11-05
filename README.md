# DjangoLMS

Проект Django с улучшенной структурой, раздельными настройками и унифицированным форматом ответов API.

## Что изменено

- Единое виртуальное окружение: `.venv` (активация в Windows PowerShell: `..\.venv\Scripts\Activate.ps1`)
- Фиксированные зависимости в `requirements.txt`
- Настройки разбиты на `lms_project/settings/{base,dev,prod}.py` и читают переменные из `.env` (через `django-environ`)
- По умолчанию используется профиль `dev`: `lms_project.settings.dev`
- Единый формат ответов API: `{ success, message, code, result }` (для ошибок также поле `errors`)

## Быстрый старт

1) Создайте файл окружения:
- Скопируйте `.env.example` → `.env` и при необходимости измените значения

2) Установите зависимости в локальное окружение:
- Windows PowerShell: `..\.venv\Scripts\python.exe -m pip install -r requirements.txt`

3) Примените миграции и запустите сервер:
- `python manage.py migrate`
- `python manage.py runserver`

Без активации окружения можно вызывать явный интерпретатор:

```
..\.venv\Scripts\python.exe manage.py runserver
```

## Настройки

- `base.py` — общие настройки; читает `.env` (переменные: `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, опционально `DATABASE_URL`)
- `dev.py` — режим разработки (DEBUG=True, разрешены все хосты)
- `prod.py` — продакшен (DEBUG=False; задайте `ALLOWED_HOSTS` и `SECRET_KEY` в `.env`)

Сменить профиль можно через переменную окружения `DJANGO_SETTINGS_MODULE`, например:
- `lms_project.settings.prod`

## Единый формат ответов API

Все ответы API приводятся к единому виду:

```
{
  "success": true | false,
  "message": "текст",
  "code": <HTTP-код>,
  "result": <данные или null>,
  "errors": <подробности об ошибке, опционально>
}
```

Реализовано через хелперы `success(...)`/`error(...)` в `lms_project/api.py` и глобальный обработчик исключений DRF `lms_project/exceptions.py`.

## Аутентификация (JWT)

- `POST /api/auth/register/` — регистрирует пользователя и сразу возвращает токены
  - Тело: `username`, `email`, `password`, `password2`
  - Ответ (201): `{ success, message, code, result: { access, refresh, user } }`
- `POST /api/auth/login/` — вход по `email` + `password` (возвращает `access` и `refresh`)
- `POST /api/auth/token/refresh/` — обновление `access` по `refresh`
- `POST /api/auth/logout/` — добавляет `refresh` в чёрный список (нужен заголовок `Authorization: Bearer <access>`)

Подключено приложение чёрного списка: `rest_framework_simplejwt.token_blacklist` (миграции применены).

## Полезно знать

- Активировать окружение: `..\.venv\Scripts\Activate.ps1`
- Проверить Django: `python -m pip show django`
- Переменные `.env`:
  - `SECRET_KEY` — секретный ключ Django
  - `DEBUG` — `True/False`
  - `ALLOWED_HOSTS` — список хостов через запятую (например: `127.0.0.1,localhost`)
  - `DATABASE_URL` — опционально, например для Postgres: `postgres://user:pass@localhost:5432/djangolms`
