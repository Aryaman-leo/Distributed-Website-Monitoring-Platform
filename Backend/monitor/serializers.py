from rest_framework import serializers
from .models import Website, MonitorResult


class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = ('id', 'url', 'is_active', 'created_at')
        read_only_fields = ('id', 'created_at')


class MonitorResultSerializer(serializers.ModelSerializer):
    website_url = serializers.CharField(source='website.url', read_only=True)
    status_display = serializers.CharField(source='status_display', read_only=True)
    ssl_display = serializers.CharField(source='ssl_display', read_only=True)
    response_time_display = serializers.CharField(source='response_time_display', read_only=True)

    class Meta:
        model = MonitorResult
        fields = (
            'id',
            'website',
            'website_url',
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
        read_only_fields = ('id', 'checked_at')
