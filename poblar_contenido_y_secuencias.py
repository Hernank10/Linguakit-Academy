#!/usr/bin/env python3
"""
Script para:
- Agregar contenido enriquecido a lecciones (si existe el campo)
- Mejorar ejercicios con explicaciones detalladas
- Crear secuencias didácticas agrupando lecciones
"""

import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linguakit.settings')
import django
django.setup()

from django.db import transaction
from apps.content.models import Curso, Leccion, Ejercicio
from apps.contenidos.models import SecuenciaDidactica

print("=" * 70)
print("📝 POBLANDO CONTENIDO Y CREANDO SECUENCIAS DIDÁCTICAS")
print("=" * 70)

# ============================================================
# 1. VERIFICAR CAMPOS
# ============================================================
print("\n📦 1. Verificando campos de los modelos...")

leccion_has_contenido = hasattr(Leccion, 'contenido')
ejercicio_has_explicacion = hasattr(Ejercicio, 'explicacion')

print(f"   Leccion tiene campo 'contenido': {leccion_has_contenido}")
print(f"   Ejercicio tiene campo 'explicacion': {ejercicio_has_explicacion}")

# ============================================================
# 2. AGREGAR CONTENIDO A LECCIONES (si existe el campo)
# ============================================================
print("\n📖 2. Agregando contenido a lecciones...")

lecciones_actualizadas = 0
if leccion_has_contenido:
    for leccion in Leccion.objects.all():
        if not leccion.contenido or len(leccion.contenido) < 50:
            contenido = f"""
<h3>{leccion.titulo}</h3>
<p><strong>Objetivos:</strong> Comprender y aplicar los conceptos de {leccion.titulo}.</p>
<h4>📚 Desarrollo</h4>
<p>{leccion.descripcion or f"Exploramos el tema de {leccion.titulo} aplicado a la morfosintaxis."}</p>
<h4>📝 Ejemplos prácticos</h4>
<ul><li>Ejemplo 1: Análisis de oraciones.</li><li>Ejemplo 2: Identificación de funciones.</li></ul>
<h4>🔍 Actividades</h4>
<ul><li>Analiza 3 oraciones con la estructura vista.</li><li>Completa los ejercicios propuestos.</li></ul>
"""
            leccion.contenido = contenido
            leccion.save()
            lecciones_actualizadas += 1
    print(f"   ✅ {lecciones_actualizadas} lecciones actualizadas")
else:
    print("   ℹ️ El campo 'contenido' no existe en Leccion. Omitiendo.")

# ============================================================
# 3. MEJORAR EJERCICIOS (si existe explicacion)
# ============================================================
print("\n📝 3. Mejorando ejercicios...")

ejercicios_actualizados = 0
if ejercicio_has_explicacion:
    for ejercicio in Ejercicio.objects.all():
        if not ejercicio.explicacion or len(ejercicio.explicacion) < 20:
            ejercicio.explicacion = f"✅ Respuesta correcta: '{ejercicio.respuesta_correcta}'. " \
                                    f"Este ejercicio evalúa tu comprensión sobre {ejercicio.leccion.titulo[:30]}."
            ejercicio.save()
            ejercicios_actualizados += 1
    print(f"   ✅ {ejercicios_actualizados} ejercicios mejorados")
else:
    print("   ℹ️ El campo 'explicacion' no existe en Ejercicio. Omitiendo.")

# ============================================================
# 4. CREAR SECUENCIAS DIDÁCTICAS
# ============================================================
print("\n📋 4. Creando secuencias didácticas...")

secuencias_creadas = 0
secuencias_omitidas = 0

# Verificar la relación entre SecuenciaDidactica y Leccion
# Puede ser ManyToMany ('lecciones') o ForeignKey ('leccion')
tiene_many = hasattr(SecuenciaDidactica, 'lecciones')
tiene_fk = hasattr(SecuenciaDidactica, 'leccion')

print(f"   SecuenciaDidactica tiene ManyToMany 'lecciones': {tiene_many}")
print(f"   SecuenciaDidactica tiene ForeignKey 'leccion': {tiene_fk}")

for curso in Curso.objects.all():
    lecciones = Leccion.objects.filter(curso=curso).order_by('orden')
    total = lecciones.count()
    if total == 0:
        continue

    # Agrupar en bloques de 3 a 5
    num_grupos = max(1, total // 3)
    tamanio = max(3, total // num_grupos)

    for i in range(0, total, tamanio):
        grupo = list(lecciones[i:i + tamanio])
        if not grupo:
            continue

        titulo = f"Secuencia {i//tamanio + 1}: {curso.titulo[:30]}"
        descripcion = f"Agrupa las lecciones {grupo[0].orden} a {grupo[-1].orden} del curso '{curso.titulo}'."

        # Crear o actualizar secuencia
        secuencia, created = SecuenciaDidactica.objects.get_or_create(
            titulo=titulo,
            defaults={
                'descripcion': descripcion,
                'curso': curso,
            }
        )

        if created:
            secuencias_creadas += 1
        else:
            # Si ya existe, actualizar descripción
            secuencia.descripcion = descripcion
            secuencia.save()

        # Asignar lecciones según el tipo de relación
        if tiene_many:
            # ManyToMany: añadir todas las lecciones del grupo
            secuencia.lecciones.add(*grupo)
        elif tiene_fk:
            # ForeignKey: solo puede tener una lección, crear una secuencia por lección
            # En este caso, mejor crear una secuencia por cada lección individual
            # Pero como ya estamos agrupando, no usamos FK aquí.
            # Dejamos como está y solo asignamos la primera lección (opcional)
            pass

    # Si es ForeignKey, crear secuencias individuales para cada lección
    if tiene_fk:
        for leccion in lecciones:
            secuencia, created = SecuenciaDidactica.objects.get_or_create(
                leccion=leccion,
                defaults={
                    'titulo': f"Secuencia: {leccion.titulo[:40]}",
                    'descripcion': f"Secuencia individual para la lección {leccion.titulo}",
                    'curso': curso,
                }
            )
            if created:
                secuencias_creadas += 1

print(f"   ✅ {secuencias_creadas} secuencias didácticas creadas/actualizadas")

# ============================================================
# 5. REGISTRO EN ADMIN (sugerencia)
# ============================================================
print("\n⚙️ 5. Sugerencia para el admin:")
print("   Asegúrate de que los modelos estén registrados en admin.py:")
print("""
# apps/content/admin.py
from django.contrib import admin
from .models import Curso, Leccion, Ejercicio

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['id', 'titulo', 'categoria', 'nivel']
    search_fields = ['titulo', 'descripcion']

@admin.register(Leccion)
class LeccionAdmin(admin.ModelAdmin):
    list_display = ['id', 'titulo', 'curso', 'orden']
    list_filter = ['curso']

@admin.register(Ejercicio)
class EjercicioAdmin(admin.ModelAdmin):
    list_display = ['id', 'titulo', 'leccion', 'puntos']
    list_filter = ['leccion']
""")

print("""
# apps/contenidos/admin.py
from django.contrib import admin
from .models import SecuenciaDidactica

@admin.register(SecuenciaDidactica)
class SecuenciaDidacticaAdmin(admin.ModelAdmin):
    list_display = ['id', 'titulo', 'curso']
    search_fields = ['titulo']
    filter_horizontal = ['lecciones']  # si es ManyToMany
""")

# ============================================================
# 6. ESTADÍSTICAS FINALES
# ============================================================
print("\n" + "=" * 70)
print("📊 ESTADÍSTICAS FINALES")
print("=" * 70)

total_cursos = Curso.objects.count()
total_lecciones = Leccion.objects.count()
total_ejercicios = Ejercicio.objects.count()
total_secuencias = SecuenciaDidactica.objects.count()

print(f"   📚 Cursos: {total_cursos}")
print(f"   📖 Lecciones: {total_lecciones}")
print(f"   📝 Ejercicios: {total_ejercicios}")
print(f"   📋 Secuencias Didácticas: {total_secuencias}")
print("=" * 70)
print("✅ ¡CONTENIDO POBLADO Y SECUENCIAS CREADAS!")
