from django.urls import path
from . import views

urlpatterns = [
    # Web UI routes only (API is in soc_platform/urls.py)
    path('', views.alert_list, name='alert_list'),
    path('create/', views.create_alert, name='create_alert'),
]