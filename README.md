# DjangoLMS

Opinionated cleanup of structure for easier local dev and deployment.

## What Changed

- Single virtualenv: `.venv` (Windows activation: `..\.venv\Scripts\Activate.ps1`)
- Requirements pinned in `requirements.txt`
- Settings split into `lms_project/settings/{base,dev,prod}.py` with `.env` support via `django-environ`
- Default settings module for local runs: `lms_project.settings.dev`
- Cleaned up unreadable comments in `core/` and `urls`

## Quickstart

1. Create `.env` from template and adjust values:
   - Copy `.env.example` to `.env`
2. Install deps in local venv:
   - Windows PowerShell: `..\.venv\Scripts\python.exe -m pip install -r requirements.txt`
3. Migrate and run:
   - `python manage.py migrate`
   - `python manage.py runserver`

If you don’t want to activate the venv, use the explicit interpreter:

```
..\.venv\Scripts\python.exe manage.py runserver
```

## Settings

- `base.py`: shared settings; reads from `.env` (SECRET_KEY, DEBUG, ALLOWED_HOSTS, DATABASE_URL)
- `dev.py`: DEBUG on, permissive hosts
- `prod.py`: DEBUG off; set `ALLOWED_HOSTS` and `SECRET_KEY` via `.env`

## Auth API

- `POST /api/auth/register/` — username, email, password, password2
- `POST /api/auth/login/` — email, password (JWT access/refresh)
- `POST /api/auth/token/refresh/` — refresh → new access
- `POST /api/auth/logout/` — refresh blacklisted (requires Authorization header)

