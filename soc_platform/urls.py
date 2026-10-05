from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from alerts.views import AlertViewSet

# REST API Router (at root level)
router = DefaultRouter()
router.register(r'api/alerts', AlertViewSet, basename='alert-api')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API routes (at root)
    path('', include(router.urls)),
    
    # Web UI routes
    path('alerts/', include('alerts.urls')),
]