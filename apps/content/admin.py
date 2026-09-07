from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import Curso, Leccion, Ejercicio
from apps.core.models import Programa

# ============================================================
# 1. ADMIN DE CURSOS
# ============================================================
@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['id', 'titulo', 'categoria', 'nivel', 'created_at']
    list_filter = ['categoria', 'nivel']
    search_fields = ['titulo', 'descripcion']
    ordering = ['-created_at']

# ============================================================
# 2. ADMIN DE LECCIONES
# ============================================================
@admin.register(Leccion)
class LeccionAdmin(admin.ModelAdmin):
    list_display = ['id', 'titulo', 'curso', 'orden', 'created_at']
    list_filter = ['curso']
    search_fields = ['titulo', 'descripcion']
    ordering = ['curso', 'orden']

# ============================================================
# 3. FILTRO PERSONALIZADO POR PROGRAMA
# ============================================================
class ProgramaFilter(SimpleListFilter):
    title = 'Programa'
    parameter_name = 'programa'

    def lookups(self, request, model_admin):
        return [(p.id, p.nombre) for p in Programa.objects.all().order_by('nombre')]

    def queryset(self, request, queryset):
        if self.value():
            programa = Programa.objects.get(id=self.value())
            return queryset.filter(leccion__curso__categoria__icontains=programa.nombre[:20])
        return queryset

# ============================================================
# 4. ADMIN DE EJERCICIOS (SÓLO UNA VEZ)
# ============================================================
@admin.register(Ejercicio)
class EjercicioAdmin(admin.ModelAdmin):
    list_display = ['id', 'titulo', 'leccion', 'puntos', 'created_at']
    list_filter = [ProgramaFilter, 'leccion']  # Ahora puedes filtrar por Programa
    search_fields = ['pregunta', 'respuesta_correcta', 'titulo']
    ordering = ['-created_at']
    list_per_page = 100  # Muestra 100 ejercicios por página
