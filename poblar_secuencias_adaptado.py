#!/usr/bin/env python3
"""
Script para crear una secuencia didáctica por programa.
- Cada programa tendrá una única secuencia.
- Se usa `get_or_create` con `programa` como clave.
- Se actualiza `introduccion` y `objetivo_general` con contenido generado.
"""

import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linguakit.settings')
import django
django.setup()

from apps.core.models import Programa
from apps.contenidos.models import SecuenciaDidactica
from apps.content.models import Curso

print("=" * 70)
print("📝 CREANDO SECUENCIAS DIDÁCTICAS (UNA POR PROGRAMA)")
print("=" * 70)

# ============================================================
# 1. VERIFICAR CAMPOS
# ============================================================
print("\n📦 1. Verificando campos de SecuenciaDidactica...")

campos = [f.name for f in SecuenciaDidactica._meta.fields]
print(f"   Campos disponibles: {campos}")

tiene_programa = 'programa' in campos
print(f"   Tiene campo 'programa': {tiene_programa}")

# ============================================================
# 2. OBTENER PROGRAMAS
# ============================================================
print("\n📚 2. Obteniendo Programas...")

programas = Programa.objects.all()
print(f"   Programas encontrados: {programas.count()}")

# ============================================================
# 3. CREAR UNA SECUENCIA POR PROGRAMA
# ============================================================
print("\n📋 3. Creando secuencias didácticas...")

secuencias_creadas = 0
secuencias_actualizadas = 0

for programa in programas:
    # Buscar cursos relacionados (para enriquecer la descripción)
    cursos = Curso.objects.filter(categoria__icontains=programa.nombre[:20])[:5]
    titulos = [c.titulo for c in cursos] if cursos else ["Morfosintaxis Castellana"]

    # Generar contenido rico
    introduccion = f"Secuencia didáctica para el programa '{programa.nombre}'. " \
                   f"Agrupa contenidos de morfosintaxis, redacción y literatura castellana."
    objetivo = f"Objetivo general: Desarrollar habilidades en {programa.nombre} " \
               f"a través de los cursos: {', '.join(t[:30] for t in titulos)}."

    # Crear o actualizar secuencia (clave única: programa)
    secuencia, created = SecuenciaDidactica.objects.get_or_create(
        programa=programa,
        defaults={
            'introduccion': introduccion,
            'objetivo_general': objetivo,
        }
    )

    if created:
        secuencias_creadas += 1
        print(f"   ✅ Secuencia creada para programa: {programa.nombre}")
    else:
        # Actualizar si el contenido cambió
        if secuencia.introduccion != introduccion or secuencia.objetivo_general != objetivo:
            secuencia.introduccion = introduccion
            secuencia.objetivo_general = objetivo
            secuencia.save()
            secuencias_actualizadas += 1
            print(f"   🔄 Secuencia actualizada para programa: {programa.nombre}")

# ============================================================
# 4. ESTADÍSTICAS FINALES
# ============================================================
print("\n" + "=" * 70)
print("📊 ESTADÍSTICAS FINALES")
print("=" * 70)

total_secuencias = SecuenciaDidactica.objects.count()
print(f"   📋 Secuencias Didácticas totales: {total_secuencias}")
print(f"   ✅ Secuencias creadas: {secuencias_creadas}")
print(f"   🔄 Secuencias actualizadas: {secuencias_actualizadas}")
print("=" * 70)
print("✅ ¡SECUENCIAS DIDÁCTICAS CREADAS/ACTUALIZADAS!")
