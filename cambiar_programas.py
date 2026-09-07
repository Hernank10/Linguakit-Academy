#!/usr/bin/env python3
"""
Script para reemplazar todos los programas existentes por 50 nuevos programas
enfocados en Morfosintaxis, Redacción y Literatura Castellana.
"""

import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linguakit.settings')
import django
django.setup()

from apps.core.models import Programa

print("=" * 70)
print("🔄 REEMPLAZANDO PROGRAMAS POR NUEVOS PROGRAMAS")
print("=" * 70)

# ============================================================
# 1. CONFIRMACIÓN
# ============================================================

total_programas = Programa.objects.count()
if total_programas == 0:
    print("\n⚠️ No hay programas para eliminar.")
else:
    print(f"\n⚠️ Se eliminarán {total_programas} programas existentes.")
    respuesta = input("¿Estás seguro? (escribe 'si' para continuar): ").strip().lower()
    if respuesta != 'si':
        print("❌ Operación cancelada.")
        sys.exit(0)

# ============================================================
# 2. ELIMINAR PROGRAMAS EXISTENTES
# ============================================================

print("\n🗑️ Eliminando programas existentes...")
programas_eliminados = Programa.objects.all().delete()
print(f"✅ Eliminados: {programas_eliminados[0]} programas")

# ============================================================
# 3. DEFINIR NUEVOS PROGRAMAS (50)
# ============================================================

NUEVOS_PROGRAMAS = [
    # === MORFOSINTAXIS (20) ===
    {"nombre": "Fundamentos de Morfosintaxis", "descripcion": "Estudio de la morfología y sintaxis del castellano."},
    {"nombre": "Morfología del Castellano", "descripcion": "Estructura de las palabras: lexemas, morfemas y procesos de formación."},
    {"nombre": "Sintaxis del Castellano", "descripcion": "Estructura de las oraciones y sus constituyentes."},
    {"nombre": "Análisis Morfosintáctico", "descripcion": "Técnicas para analizar oraciones desde la perspectiva morfosintáctica."},
    {"nombre": "Categorías Gramaticales", "descripcion": "Clasificación de las palabras según su función morfosintáctica."},
    {"nombre": "Sintagmas y Funciones", "descripcion": "Estudio de los sintagmas y sus funciones sintácticas."},
    {"nombre": "Oración Simple y Compuesta", "descripcion": "Análisis de oraciones simples y compuestas en castellano."},
    {"nombre": "Subordinación y Coordinación", "descripcion": "Mecanismos de subordinación y coordinación en la lengua."},
    {"nombre": "Concordancia y Régimen", "descripcion": "Reglas de concordancia y régimen verbal en castellano."},
    {"nombre": "Complementos Verbales", "descripcion": "Estudio de los complementos del verbo: directo, indirecto, de régimen, etc."},
    {"nombre": "Perífrasis Verbales", "descripcion": "Análisis de las perífrasis verbales y su estructura."},
    {"nombre": "Voz Activa y Pasiva", "descripcion": "Transformaciones de voz en la oración."},
    {"nombre": "Pronombres y Determinantes", "descripcion": "Morfosintaxis de los pronombres y determinantes."},
    {"nombre": "Adverbios y Preposiciones", "descripcion": "Funciones y usos de adverbios y preposiciones."},
    {"nombre": "Conjunciones y Conectores", "descripcion": "Morfosintaxis de los conectores discursivos."},
    {"nombre": "Oraciones Interrogativas y Exclamativas", "descripcion": "Estructura de oraciones interrogativas y exclamativas."},
    {"nombre": "Oraciones Condicionales y Concesivas", "descripcion": "Análisis de oraciones condicionales y concesivas."},
    {"nombre": "Oraciones Causales y Finales", "descripcion": "Estructura de oraciones causales y finales."},
    {"nombre": "Oraciones Temporales y Modales", "descripcion": "Análisis de oraciones temporales y modales."},
    {"nombre": "Morfosintaxis Aplicada", "descripcion": "Aplicación práctica de conceptos morfosintácticos en textos reales."},

    # === REDACCIÓN (15) ===
    {"nombre": "Redacción Académica", "descripcion": "Técnicas de redacción para trabajos académicos y científicos."},
    {"nombre": "Redacción Periodística", "descripcion": "Escritura de noticias, reportajes y artículos de opinión."},
    {"nombre": "Redacción Creativa", "descripcion": "Técnicas de escritura literaria y narrativa."},
    {"nombre": "Redacción Científica", "descripcion": "Redacción de artículos, informes y proyectos científicos."},
    {"nombre": "Redacción Corporativa", "descripcion": "Comunicación escrita en el ámbito empresarial."},
    {"nombre": "Redacción Digital", "descripcion": "Escritura para medios digitales, blogs y redes sociales."},
    {"nombre": "Redacción de Ensayos", "descripcion": "Estructura y técnicas para escribir ensayos argumentativos."},
    {"nombre": "Redacción de Informes", "descripcion": "Elaboración de informes técnicos y profesionales."},
    {"nombre": "Redacción de Cartas y Correos", "descripcion": "Escritura formal de cartas y correos electrónicos."},
    {"nombre": "Redacción de Discursos", "descripcion": "Técnicas para redactar discursos efectivos."},
    {"nombre": "Redacción de Guiones", "descripcion": "Escritura de guiones para cine, televisión y radio."},
    {"nombre": "Redacción de Poesía", "descripcion": "Técnicas de escritura poética y verso."},
    {"nombre": "Redacción de Cuentos", "descripcion": "Estructura y técnicas para escribir cuentos."},
    {"nombre": "Redacción de Novelas", "descripcion": "Planificación y desarrollo de novelas."},
    {"nombre": "Redacción de Artículos de Opinión", "descripcion": "Escritura de columnas y artículos de opinión."},

    # === LITERATURA CASTELLANA (15) ===
    {"nombre": "Literatura Española Medieval", "descripcion": "Estudio de la literatura española desde sus orígenes hasta el siglo XV."},
    {"nombre": "Literatura del Siglo de Oro", "descripcion": "Autores y obras del Siglo de Oro español."},
    {"nombre": "Literatura del Romanticismo", "descripcion": "Movimiento romántico en la literatura española."},
    {"nombre": "Literatura del Realismo", "descripcion": "Novela realista y naturalista en España."},
    {"nombre": "Literatura del Modernismo", "descripcion": "Corriente modernista en la literatura hispánica."},
    {"nombre": "Literatura de la Generación del 98", "descripcion": "Autores y obras de la Generación del 98."},
    {"nombre": "Literatura de la Generación del 27", "descripcion": "Poesía y prosa de la Generación del 27."},
    {"nombre": "Literatura Hispanoamericana", "descripcion": "Autores y obras clave de Latinoamérica."},
    {"nombre": "Literatura Hispanoamericana Contemporánea", "descripcion": "Tendencias actuales de la literatura hispanoamericana."},
    {"nombre": "Poesía Española", "descripcion": "Análisis de la poesía española a lo largo de los siglos."},
    {"nombre": "Teatro Español", "descripcion": "Estudio del teatro español desde sus orígenes."},
    {"nombre": "Novela Española", "descripcion": "Evolución de la novela en España."},
    {"nombre": "Literatura Infantil y Juvenil", "descripcion": "Obras de literatura infantil y juvenil en castellano."},
    {"nombre": "Literatura de Viajes", "descripcion": "Relatos de viajes en la literatura hispánica."},
    {"nombre": "Literatura y Cine", "descripcion": "Relación entre literatura y cine en el mundo hispánico."},
]

# ============================================================
# 4. CREAR NUEVOS PROGRAMAS
# ============================================================

print("\n📁 Creando 50 nuevos programas...")

creados = 0
for data in NUEVOS_PROGRAMAS:
    programa, created = Programa.objects.get_or_create(
        nombre=data['nombre'],
        defaults={'descripcion': data['descripcion']}
    )
    if created:
        creados += 1
        print(f"  ✅ Programa creado: {programa.nombre}")

print(f"\n✅ {creados} programas creados exitosamente.")

# ============================================================
# 5. RESUMEN FINAL
# ============================================================

total_actual = Programa.objects.count()
print("\n" + "=" * 70)
print("📊 RESUMEN FINAL")
print("=" * 70)
print(f"   📁 Programas actuales: {total_actual}")
print(f"   📁 Programas esperados: 50")
print("=" * 70)
print("✅ ¡PROGRAMAS REEMPLAZADOS EXITOSAMENTE!")

# Mostrar lista de programas
print("\n📋 Lista de programas creados:")
for p in Programa.objects.all().order_by('nombre'):
    print(f"   - {p.nombre}")
