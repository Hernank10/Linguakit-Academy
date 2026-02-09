from django.contrib import admin
from .models import Leccion, Ejercicio
from apps.core.models import Programa

@admin.register(Leccion)
class LeccionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'programa', 'orden')
    list_filter = ('programa',)
    search_fields = ('titulo', 'contenido_teorico')

@admin.register(Ejercicio)
class EjercicioAdmin(admin.ModelAdmin):
    list_display = ('pregunta', 'leccion', 'solucion')
    list_filter = ('leccion__programa',)

# Opcional: Si quieres gestionar Cursos (Programas) desde aquí también
