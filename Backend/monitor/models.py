from django.db import models

class Website(models.Model):
    url = models.URLField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.url


class MonitorResult(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    status_code = models.IntegerField(help_text="HTTP status (0 = connection/SSL error)")
    response_time = models.FloatField(help_text="Response time in seconds")
    checked_at = models.DateTimeField(auto_now_add=True)
    # Extra detail for readable reports
    final_url = models.URLField(max_length=1000, blank=True, help_text="URL after redirects")
    ssl_valid = models.BooleanField(
        null=True,
        blank=True,
        help_text="True/False for HTTPS; empty for HTTP or when check failed before SSL",
    )
    error_message = models.CharField(
        max_length=500,
        blank=True,
        help_text="Error details when status_code is 0 (e.g. timeout, SSL failure)",
    )

    def __str__(self):
        return f"{self.website.url} — {self.status_code} — {self.response_time}s"

    @property
    def status_display(self):
        if self.status_code == 0:
            return "Down / Error"
        if 200 <= self.status_code < 300:
            return "OK"
        if 300 <= self.status_code < 400:
            return "Redirect"
        if 400 <= self.status_code < 500:
            return "Client Error"
        if self.status_code >= 500:
            return "Server Error"
        return "Unknown"

    @property
    def ssl_display(self):
        if self.ssl_valid is None:
            return "—"
        return "Valid" if self.ssl_valid else "Invalid / Error"

    @property
    def response_time_display(self):
        return f"{self.response_time:.3f} s"
