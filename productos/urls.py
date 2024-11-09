from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.productos),
    path('productos/<int:id>', views.detalles_productos)
]