from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('curso/<int:curso_id>/', views.curso_detalle, name='curso_detalle'),
]
