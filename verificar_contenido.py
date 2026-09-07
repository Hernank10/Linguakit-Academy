#!/usr/bin/env python3
"""
Script para verificar y mostrar estadísticas del contenido:
- Programas
- Cursos
- Lecciones
- Ejercicios
"""

import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linguakit.settings')
import django
django.setup()

from django.db.models import Count
from apps.core.models import Programa
from apps.content.models import Curso, Leccion, Ejercicio

print("=" * 70)
print("📊 VERIFICACIÓN DE CONTENIDO")
print("=" * 70)

# ============================================================
# 1. PROGRAMAS
# ============================================================
print("\n📁 1. PROGRAMAS")
print("-" * 50)

total_programas = Programa.objects.count()
print(f"Total: {total_programas}")

if total_programas > 0:
    print("\nLista de programas:")
    for p in Programa.objects.all().order_by('nombre')[:10]:
        print(f"  - {p.nombre}")
    if total_programas > 10:
        print(f"  ... y {total_programas - 10} más")

# ============================================================
# 2. CURSOS
# ============================================================
print("\n📚 2. CURSOS")
print("-" * 50)

total_cursos = Curso.objects.count()
print(f"Total: {total_cursos}")

# Cursos por categoría
categorias = Curso.objects.values('categoria').annotate(total=Count('id')).order_by('-total')
print("\nCursos por categoría:")
for cat in categorias:
    print(f"  - {cat['categoria']}: {cat['total']} cursos")

# Últimos 5 cursos
print("\nÚltimos 5 cursos creados:")
for c in Curso.objects.all().order_by('-id')[:5]:
    lecciones_count = Leccion.objects.filter(curso=c).count()
    print(f"  - {c.titulo[:50]} (ID: {c.id}) - Lecciones: {lecciones_count}")

# ============================================================
# 3. LECCIONES
# ============================================================
print("\n📖 3. LECCIONES")
print("-" * 50)

total_lecciones = Leccion.objects.count()
print(f"Total: {total_lecciones}")

# Cursos con más lecciones
print("\nCursos con más lecciones:")
for c in Curso.objects.annotate(num_lecciones=Count('lecciones')).order_by('-num_lecciones')[:5]:
    print(f"  - {c.titulo[:50]}: {c.num_lecciones} lecciones")

# Últimas 5 lecciones
print("\nÚltimas 5 lecciones creadas:")
for l in Leccion.objects.all().order_by('-id')[:5]:
    ejercicios_count = Ejercicio.objects.filter(leccion=l).count()
    print(f"  - {l.titulo[:50]} (ID: {l.id}) - Ejercicios: {ejercicios_count}")

# ============================================================
# 4. EJERCICIOS
# ============================================================
print("\n📝 4. EJERCICIOS")
print("-" * 50)

total_ejercicios = Ejercicio.objects.count()
print(f"Total: {total_ejercicios}")

# Estadísticas generales
print("\nEstadísticas generales:")
# Lecciones con más ejercicios
lecciones_top = Leccion.objects.annotate(num_ejercicios=Count('ejercicios')).order_by('-num_ejercicios')[:5]
print("\nLecciones con más ejercicios:")
for l in lecciones_top:
    print(f"  - {l.titulo[:50]}: {l.num_ejercicios} ejercicios")

# Promedio de ejercicios por lección
from django.db.models import Avg
avg_ejercicios = Leccion.objects.annotate(num_ejercicios=Count('ejercicios')).aggregate(Avg('num_ejercicios'))
if avg_ejercicios['num_ejercicios__avg']:
    print(f"\nPromedio de ejercicios por lección: {avg_ejercicios['num_ejercicios__avg']:.2f}")

# ============================================================
# 5. ESTADÍSTICAS DE EJERCICIOS POR TIPO (si existe el campo)
# ============================================================
print("\n📊 5. TIPOS DE EJERCICIOS")
print("-" * 50)

# Verificar si existe el campo 'tipo' en Ejercicio
try:
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA table_info(content_ejercicio)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'tipo' in columns:
            tipos = Ejercicio.objects.values('tipo').annotate(total=Count('id')).order_by('-total')
            print("Distribución por tipo:")
            for t in tipos:
                print(f"  - {t['tipo']}: {t['total']} ejercicios")
        else:
            print("  ℹ️ El campo 'tipo' no existe en el modelo Ejercicio")
except Exception as e:
    print(f"  ⚠️ No se pudo verificar tipos: {e}")

# ============================================================
# 6. RESUMEN FINAL
# ============================================================
print("\n" + "=" * 70)
print("📊 RESUMEN FINAL")
print("=" * 70)
print(f"   📁 Programas: {total_programas}")
print(f"   📚 Cursos: {total_cursos}")
print(f"   📖 Lecciones: {total_lecciones}")
print(f"   📝 Ejercicios: {total_ejercicios}")
print("=" * 70)
print("✅ VERIFICACIÓN COMPLETADA")
