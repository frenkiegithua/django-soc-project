from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from alerts.views import AlertViewSet, IncidentViewSet, alert_stats

# REST API Router
router = DefaultRouter()
router.register(r'api/alerts', AlertViewSet, basename='alert-api')
router.register(r'api/incidents', IncidentViewSet, basename='incident-api')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API routes
    path('', include(router.urls)),
    path('api/stats/', alert_stats, name='alert-stats'),
    
    # Web UI routes
    path('alerts/', include('alerts.urls')),
]