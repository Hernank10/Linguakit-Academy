from django.contrib import admin
from .models import Programa
from apps.cursos.models import Leccion

class LeccionInline(admin.TabularInline):
    model = Leccion
    extra = 1
    show_change_link = True

@admin.register(Programa)
class ProgramaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'activo')
    list_filter = ('tipo', 'activo')
    inlines = [LeccionInline]
