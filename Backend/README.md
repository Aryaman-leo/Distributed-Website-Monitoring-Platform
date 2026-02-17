# Distributed Website Monitoring Platform

A scalable distributed system that monitors websites for uptime and performance using Django, Redis, and Celery.

## Architecture

```
User → Django API → PostgreSQL/SQLite → Redis Queue → Celery Workers → Target Websites
```

- **Django**: REST API, website and result storage
- **PostgreSQL** (or SQLite in dev): `Website`, `MonitorResult` tables
- **Redis**: Celery broker and result backend
- **Celery workers**: Run `check_website` tasks with retries
- **Celery Beat**: Schedules checks every 60 seconds for all active websites

## Setup

1. **Create virtualenv and install dependencies**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```

2. **Environment (optional)**

   Create a `.env` file for overrides:

   - `DATABASE_URL` – PostgreSQL URL (e.g. `postgresql://user:pass@localhost/db`). If unset, SQLite is used.
   - `CELERY_BROKER_URL` – default `redis://localhost:6379/0`
   - `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` – Django settings

3. **Database**

   ```bash
   python manage.py migrate
   python manage.py createsuperuser   # optional, for /admin
   ```

4. **Run services**

   - **Django**  
     `python manage.py runserver`

   - **Redis**  
     Ensure Redis is running (e.g. `redis-server` or Docker).

   - **Celery worker**  
     `celery -A config worker -l info`

   - **Celery Beat** (scheduler)  
     `celery -A config beat -l info`  
     Or run worker and beat together:  
     `celery -A config worker --beat -l info`

## REST API

- **Websites**
  - `GET /api/websites/` – list websites
  - `POST /api/websites/` – add website (`{"url": "https://example.com", "is_active": true}`)
  - `GET /api/websites/{id}/` – retrieve one
  - `PATCH /api/websites/{id}/` – update (e.g. `is_active`)
  - `DELETE /api/websites/{id}/` – delete
  - `POST /api/websites/{id}/check_now/` – trigger an immediate check

- **Results**
  - `GET /api/results/` – list monitoring results (paginated)
  - `GET /api/results/?website_id=1` – filter by website
  - `GET /api/results/{id}/` – retrieve one

## Execution flow

1. User adds a website via `POST /api/websites/`.
2. Website is stored; Celery Beat runs every 60 seconds.
3. Beat calls `schedule_website_checks`, which queues `check_website` for each active website.
4. Workers run `check_website`: HTTP GET, measure response time, store `MonitorResult`.
5. Results are available via `GET /api/results/` and optional `?website_id=`.

## Tech stack

- **Backend**: Django, Django REST Framework  
- **Database**: PostgreSQL (production) / SQLite (dev)  
- **Queue**: Redis  
- **Workers**: Celery (with retries and Beat)

## Resume description

- Built a distributed monitoring system using Django, Redis, and Celery to automate website uptime and performance checks.
- Implemented scalable backend services and asynchronous workers for reliable infrastructure monitoring.
