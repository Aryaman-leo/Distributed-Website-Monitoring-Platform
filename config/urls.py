from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from monitor import views

router = DefaultRouter()
router.register(r'websites', views.WebsiteViewSet, basename='website')
router.register(r'results', views.MonitorResultViewSet, basename='monitorresult')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
