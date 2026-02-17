from django.urls import path, include
from django.shortcuts import redirect
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from monitor import views

router = DefaultRouter()
router.register(r'websites', views.WebsiteViewSet, basename='website')
router.register(r'results', views.MonitorResultViewSet, basename='monitorresult')

urlpatterns = [
    path('', lambda request: redirect('/api/', permanent=False)),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
