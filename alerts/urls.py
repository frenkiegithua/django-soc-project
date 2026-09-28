from django.urls import path
from . import views

urlpatterns = [
    path('', views.alert_list, name='alert_list'),
    path('create/', views.create_alert, name='create_alert'),
]