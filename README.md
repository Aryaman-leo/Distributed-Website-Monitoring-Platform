# Distributed Website Monitoring Platform

A scalable backend system that monitors websites for uptime, performance, and SSL validity using Django, Redis, and Celery. Websites can be added via API or admin panel, and checks run automatically every 60 seconds.

---

# Overview

This platform continuously monitors websites and stores detailed metrics such as status code, response time, SSL validity, redirects, and error information. It uses asynchronous workers to ensure scalability, reliability, and fault tolerance.

---

# Features

## Uptime Monitoring
Detect when a website is down, unreachable, or responding slowly.

## Performance Tracking
Measure and store response time for every check.

## SSL Certificate Validation
Verify SSL certificate validity for HTTPS websites.

## REST API
Add websites, trigger checks, and retrieve monitoring results programmatically.

## Automated Scheduling
Celery Beat schedules monitoring tasks automatically every 60 seconds.

## Fault Tolerant
Failures in one website check do not affect others due to asynchronous task processing.

---

# Architecture

```
User (API / Admin)
        │
        ▼
Django REST API
        │
        ▼
Database (PostgreSQL / SQLite)
        │
        ▼
Redis (Message Broker)
        │
        ▼
Celery Workers
        │
        ▼
Website Monitoring Tasks
        │
        ▼
Monitor Results Storage

Celery Beat → Schedules checks every 60 seconds
```

---

# Stored Monitoring Data

Each monitoring result contains:

| Field | Description |
|------|-------------|
| Website | Monitored website URL |
| Status Code | HTTP response code (200, 404, 500, etc.) |
| Status | OK, Redirect, Client Error, Server Error, Down |
| Response Time | Time taken to respond (seconds) |
| SSL Status | Valid or Invalid SSL certificate |
| Final URL | Final URL after redirects |
| Error Message | Timeout, connection error, SSL error, etc. |
| Checked At | Timestamp of the check |

---

# Tech Stack

| Layer | Technology |
|------|------------|
| Backend | Django, Django REST Framework |
| Database | PostgreSQL (Production), SQLite (Development) |
| Queue | Redis |
| Workers | Celery |
| Scheduler | Celery Beat |

---

# Project Structure

```
Backend/
│
├── config/
│   ├── settings.py
│   ├── celery.py
│   └── urls.py
│
├── monitor/
│   ├── models.py
│   ├── tasks.py
│   ├── views.py
│   ├── serializers.py
│   └── admin.py
│
├── manage.py
└── requirements.txt
```

---

# Installation

## 1. Clone Repository

```
git clone https://github.com/YOUR_USERNAME/distributed-monitoring-platform.git
cd distributed-monitoring-platform/Backend
```

---

## 2. Create Virtual Environment

```
python -m venv .venv
```

Activate environment (Windows)

```
.venv\Scripts\activate
```

Activate environment (Linux / macOS)

```
source .venv/bin/activate
```

---

## 3. Install Dependencies

```
pip install -r requirements.txt
```

---

## 4. Setup Database

```
python manage.py migrate
```

Create admin user (optional)

```
python manage.py createsuperuser
```

---

## 5. Run Services

Start Redis

```
redis-server
```

Start Django server

```
python manage.py runserver
```

Start Celery Worker

```
celery -A config worker -l info
```

Start Celery Beat Scheduler

```
celery -A config beat -l info
```

---

# API Endpoints

Base URL

```
http://localhost:8000/api/
```

---

## Websites

Get all websites

```
GET /api/websites/
```

Add new website

```
POST /api/websites/

{
  "url": "https://example.com",
  "is_active": true
}
```

Get website

```
GET /api/websites/{id}/
```

Update website

```
PATCH /api/websites/{id}/
```

Delete website

```
DELETE /api/websites/{id}/
```

Trigger manual check

```
POST /api/websites/{id}/check_now/
```

---

## Monitoring Results

Get all results

```
GET /api/results/
```

Filter results by website

```
GET /api/results/?website_id={id}
```

Get single result

```
GET /api/results/{id}/
```

---

# Admin Panel

Access admin panel

```
http://localhost:8000/admin/
```

Features

• Add and manage websites  
• View monitoring results  
• Enable or disable monitoring  

---

# How It Works

1. User adds website via API or admin  
2. Celery Beat schedules monitoring tasks every 60 seconds  
3. Celery Worker executes monitoring tasks  
4. Website is checked for uptime, performance, and SSL  
5. Results are stored in database  
6. Results are accessible via API or admin  

---

# Production Recommendations

Use PostgreSQL instead of SQLite  
Deploy Redis using Docker or managed service  
Use Gunicorn + Nginx for Django  
Run Celery workers with Supervisor or Systemd  

---

# Complete Hosted Deployment Guide (Render + Netlify)

This repo is split as:

- Backend (Django/Celery/Redis/Postgres): hosted on Render
- Landing page (static `index.html`): hosted on Netlify

## A) Backend deployment on Render (no shortcuts)

### 1. Push all required files

Ensure these files are pushed to GitHub:

- `render.yaml`
- `Backend/config/wsgi.py`
- `Backend/config/settings.py`
- `Backend/requirements.txt`
- `Backend/.env.example`

### 2. Create all services using Blueprint

1. Open Render dashboard
2. Click **New +** → **Blueprint**
3. Select your GitHub repo and branch
4. Click **Apply**

Render creates:

- `distributed-monitoring-web` (Django + Gunicorn)
- `distributed-monitoring-worker` (Celery worker)
- `distributed-monitoring-beat` (Celery beat)
- `distributed-monitoring-db` (Postgres)
- `distributed-monitoring-redis` (Redis)

### 3. Environment variables and where to get them

`render.yaml` already wires most variables:

- `SECRET_KEY`: auto-generated on web service
- `DATABASE_URL`: from Postgres connection string
- `CELERY_BROKER_URL`: from Redis connection string
- `CELERY_RESULT_BACKEND`: from Redis connection string
- `DEBUG`: set to `False`
- `ALLOWED_HOSTS`: set to `.onrender.com`

Manual check in Render:

1. Open `distributed-monitoring-web` → **Environment**
2. Confirm all vars exist
3. Reveal/copy `SECRET_KEY` only if you need it elsewhere

If you add custom domain later, update:

- `ALLOWED_HOSTS` to include your domain
- `CSRF_TRUSTED_ORIGINS` to `https://your-domain.com`

### 4. Build/start commands (already in blueprint)

- Web build: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
- Web start: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`
- Worker start: `celery -A config worker -l info`
- Beat start: `celery -A config beat -l info`

### 5. Verify backend is truly live

After deploy is healthy, open:

- `https://<your-render-service>.onrender.com/`
- `https://<your-render-service>.onrender.com/api/`
- `https://<your-render-service>.onrender.com/api/websites/`

Also check logs:

- Web logs: app boot + migrations
- Worker logs: connected to Redis
- Beat logs: scheduled checks every 60 seconds

## B) Netlify deployment (public landing page)

Your Netlify URL serves static `index.html`. It must link to your Render backend URL.

1. Open root `index.html`
2. Update `BACKEND_BASE_URL` to your real Render URL if needed
3. Push changes to GitHub
4. Redeploy Netlify

Result:

- Netlify URL = public landing page
- Render URL = real backend/API/admin

## C) Final production checklist

- [ ] Render web/worker/beat are all healthy
- [ ] Postgres and Redis are connected
- [ ] `DEBUG=False`
- [ ] `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` are correct
- [ ] Netlify links point to Render URL
- [ ] Add at least one website and verify results are generated

---

# Future Improvements

Dashboard UI (React / Next.js)  
Email alerts on downtime  
Telegram / Slack notifications  
Performance graphs  
Multi-region monitoring  

---

# License

MIT License

Free to use and modify.
