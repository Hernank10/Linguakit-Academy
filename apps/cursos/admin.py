from django.contrib import admin
from .models import Leccion, Ejercicio

class EjercicioInline(admin.TabularInline):
    model = Ejercicio
    extra = 1

@admin.register(Leccion)
class LeccionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'programa', 'orden')
    list_filter = ('programa',)
    inlines = [EjercicioInline]

admin.site.register(Ejercicio)
