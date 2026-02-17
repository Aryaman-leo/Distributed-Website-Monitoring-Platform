from django.contrib import admin
from .models import Website, MonitorResult


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('url',)


@admin.register(MonitorResult)
class MonitorResultAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'website',
        'status_display',
        'status_code',
        'response_time_display',
        'ssl_display',
        'checked_at',
    )
    list_display_links = ('id', 'website')
    list_filter = ('status_code', 'ssl_valid')
    date_hierarchy = 'checked_at'
    readonly_fields = (
        'website',
        'status_code',
        'status_display',
        'response_time',
        'response_time_display',
        'ssl_valid',
        'ssl_display',
        'final_url',
        'error_message',
        'checked_at',
    )
    fieldsets = (
        (
            'Check summary',
            {
                'fields': ('website', 'checked_at', 'status_display', 'status_code', 'response_time_display', 'response_time'),
            },
        ),
        (
            'SSL & URL',
            {
                'fields': ('ssl_display', 'ssl_valid', 'final_url'),
            },
        ),
        (
            'Error details',
            {
                'fields': ('error_message',),
                'description': 'Shown when the check failed (status code 0).',
            },
        ),
    )
