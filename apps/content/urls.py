from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    # Públicas
    path('', views.index, name='index'),
    path('categoria/<str:categoria>/', views.por_categoria, name='por_categoria'),
    path('nivel/<str:nivel>/', views.por_nivel, name='por_nivel'),
    path('tecnica/<int:id>/', views.detalle, name='detalle'),
    path('buscar/', views.buscar, name='buscar'),
    
    # Requieren autenticación
    path('dashboard/estudiante/', views.dashboard_estudiante, name='dashboard_estudiante'),
    path('dashboard/profesor/', views.dashboard_profesor, name='dashboard_profesor'),
]
