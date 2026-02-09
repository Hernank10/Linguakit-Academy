from django.contrib import admin
from .models import SecuenciaDidactica
from apps.cursos.models import Leccion, Ejercicio

class EjercicioInline(admin.TabularInline):
    model = Ejercicio
    extra = 1

class LeccionInline(admin.StackedInline):
    model = Leccion
    extra = 1
    show_change_link = True
    # Esto permite editar la lección dentro de la secuencia

@admin.register(SecuenciaDidactica)
class SecuenciaAdmin(admin.ModelAdmin):
    list_display = ('programa', 'creado_en')
    search_fields = ('programa__nombre',)
    
    # Aquí podrías usar inlines de Lecciones si vinculamos 
    # la lección a la secuencia, pero como la lección ya 
    # depende del Programa, Django lo maneja por herencia.
