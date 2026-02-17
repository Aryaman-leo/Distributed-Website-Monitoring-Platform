import requests
import time
from celery import shared_task
from django.utils import timezone
from .models import Website, MonitorResult


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def check_website(self, website_id):
    """Check a single website and store status_code, response_time, SSL, and error details."""
    try:
        website = Website.objects.get(id=website_id)
    except Website.DoesNotExist:
        return
    if not website.is_active:
        return
    start = time.time()
    status_code = 0
    final_url = ""
    ssl_valid = None
    error_message = ""
    try:
        response = requests.get(website.url, timeout=10, allow_redirects=True)
        duration = time.time() - start
        status_code = response.status_code
        final_url = response.url or ""
        ssl_valid = website.url.lower().startswith("https") if website.url else None
    except requests.exceptions.SSLError as e:
        duration = time.time() - start
        ssl_valid = False
        error_message = str(e)[:500]
    except requests.RequestException as e:
        duration = time.time() - start
        error_message = str(e)[:500]
    MonitorResult.objects.create(
        website=website,
        status_code=status_code,
        response_time=round(duration, 3),
        checked_at=timezone.now(),
        final_url=final_url or "",
        ssl_valid=ssl_valid,
        error_message=error_message,
    )


@shared_task
def schedule_website_checks():
    """Celery Beat task: queue check_website for every active website."""
    for website in Website.objects.filter(is_active=True).values_list('id', flat=True):
        check_website.delay(website)
