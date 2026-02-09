from django.urls import path
from . import views

app_name = 'cursos'

urlpatterns = [
    path('leccion/<int:leccion_id>/', views.leccion_detalle, name='leccion_detalle'),
    path('ejercicio/<int:ejercicio_id>/validar/', views.validar_ejercicio, name='validar_ejercicio'),
]
