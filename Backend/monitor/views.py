from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Website, MonitorResult
from .serializers import WebsiteSerializer, MonitorResultSerializer
from .tasks import check_website


class WebsiteViewSet(viewsets.ModelViewSet):
    """Manage websites. Add a website via POST to create and start monitoring."""
    queryset = Website.objects.all().order_by('-created_at')
    serializer_class = WebsiteSerializer

    @action(detail=True, methods=['post'])
    def check_now(self, request, pk=None):
        """Trigger an immediate check for this website."""
        website = self.get_object()
        check_website.delay(website.id)
        return Response({'status': 'check queued', 'website_id': website.id})


class MonitorResultViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only API for monitoring results. Filter by website_id via query param."""
    queryset = MonitorResult.objects.all().select_related('website').order_by('-checked_at')
    serializer_class = MonitorResultSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        website_id = self.request.query_params.get('website_id')
        if website_id:
            qs = qs.filter(website_id=website_id)
        return qs
