from django.urls import path
from . import views

urlpatterns = [
    path('ordenes/', views.ordenes),
]