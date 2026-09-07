from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    # Página de inicio
    path('', views.home, name='home'),
    
    # Técnicas
    path('tecnicas/', views.index, name='index'),
    path('tecnicas/categoria/<str:categoria>/', views.por_categoria, name='por_categoria'),
    path('tecnicas/nivel/<str:nivel>/', views.por_nivel, name='por_nivel'),
    path('tecnicas/detalle/<int:id>/', views.detalle_tecnica, name='detalle_tecnica'),
    path('tecnicas/detalle/<int:id>/', views.detalle_tecnica, name='detalle'),  # ALIAS para compatibilidad
    path('tecnicas/buscar/', views.buscar, name='buscar'),
    
    # Cursos
    path('cursos/', views.listar_cursos, name='listar_cursos'),
    path('cursos/detalle/<int:curso_id>/', views.detalle_curso, name='detalle_curso'),
    path('cursos/leccion/<int:leccion_id>/', views.detalle_leccion, name='detalle_leccion'),
    path('cursos/ejercicio/<int:ejercicio_id>/', views.detalle_ejercicio, name='detalle_ejercicio'),
    
    # Dashboards (requieren login)
    path('dashboard/estudiante/', views.dashboard_estudiante, name='dashboard_estudiante'),
    path('dashboard/profesor/', views.dashboard_profesor, name='dashboard_profesor'),
]
