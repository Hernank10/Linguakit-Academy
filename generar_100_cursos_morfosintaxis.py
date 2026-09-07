#!/usr/bin/env python3
"""
Script para eliminar todos los cursos existentes y generar 100 nuevos cursos
sobre Morfosintaxis de la Lengua Castellana, con lecciones y ejercicios.
"""

import os
import sys
import random
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linguakit.settings')
import django
django.setup()

from django.db import transaction
from apps.content.models import Curso, Leccion, Ejercicio

print("=" * 70)
print("🧹 ELIMINANDO CURSOS EXISTENTES Y GENERANDO 100 NUEVOS CURSOS")
print("=" * 70)

# ============================================================
# 1. CONFIRMACIÓN DE ELIMINACIÓN
# ============================================================

total_cursos = Curso.objects.count()
if total_cursos == 0:
    print("\n⚠️ No hay cursos para eliminar.")
else:
    print(f"\n⚠️ Se eliminarán {total_cursos} cursos, incluyendo sus lecciones y ejercicios.")
    respuesta = input("¿Estás seguro? (escribe 'si' para continuar): ").strip().lower()
    if respuesta != 'si':
        print("❌ Operación cancelada.")
        sys.exit(0)

# ============================================================
# 2. ELIMINAR CURSOS (en cascada)
# ============================================================

print("\n🗑️ Eliminando cursos...")
with transaction.atomic():
    cursos_eliminados = Curso.objects.all().delete()
    print(f"✅ Eliminados: {cursos_eliminados[0]} objetos (cursos + dependencias)")

# ============================================================
# 3. GENERAR 100 CURSOS DE MORFOSINTAXIS
# ============================================================

print("\n📚 Generando 100 cursos de Morfosintaxis Castellana...")

# Títulos de cursos sobre morfosintaxis
TITULOS_CURSOS = [
    "Introducción a la Morfosintaxis del Castellano",
    "Morfosintaxis: Estructura de las Palabras",
    "Análisis Morfosintáctico de Oraciones",
    "Morfología y Sintaxis del Español",
    "Morfosintaxis de la Lengua Castellana",
    "Categorías Gramaticales y su Función Sintáctica",
    "Sintagmas y sus Constituyentes",
    "La Oración Simple en Morfosintaxis",
    "La Oración Compuesta: Subordinación y Coordinación",
    "Concordancia y Régimen Verbal",
    "Los Complementos Verbales: Análisis Morfosintáctico",
    "Morfosintaxis del Sustantivo y el Adjetivo",
    "El Verbo: Morfología y Sintaxis",
    "Los Pronombres: Morfología y Función Sintáctica",
    "Los Determinantes: Morfosintaxis",
    "Los Conectores y su Función Sintáctica",
    "Morfosintaxis de las Perífrasis Verbales",
    "Análisis Sintáctico de Oraciones Complejas",
    "Morfosintaxis de la Subordinación Sustantiva",
    "Morfosintaxis de la Subordinación Adjetiva",
    "Morfosintaxis de la Subordinación Adverbial",
    "La Oración Pasiva: Morfosintaxis",
    "La Oración Impersonal: Morfosintaxis",
    "Morfosintaxis del Complemento Directo e Indirecto",
    "Morfosintaxis del Complemento de Régimen",
    "Morfosintaxis del Complemento Circunstancial",
    "Morfosintaxis del Atributo y Complemento Predicativo",
    "La Concordancia de Género y Número",
    "La Concordancia de Persona y Número en Verbos",
    "Morfosintaxis de los Tiempos Verbales",
    "Morfosintaxis de los Modos Verbales",
    "La Voz Activa y Pasiva en Morfosintaxis",
    "Morfosintaxis del Discurso Indirecto",
    "Morfosintaxis de las Oraciones Exclamativas e Interrogativas",
    "Morfosintaxis de las Oraciones Enunciativas",
    "Morfosintaxis de las Oraciones Desiderativas y Dubitativas",
    "Morfosintaxis de las Oraciones Condicionales",
    "Morfosintaxis de las Oraciones Concesivas",
    "Morfosintaxis de las Oraciones Consecutivas",
    "Morfosintaxis de las Oraciones Causales y Finales",
    "Morfosintaxis de las Oraciones Temporales",
    "Morfosintaxis de las Oraciones Modales",
    "Morfosintaxis de las Oraciones Comparativas",
    "Morfosintaxis de las Oraciones Ilativas",
    "Morfosintaxis de la Yuxtaposición y Coordinación",
    "Morfosintaxis de la Subordinación",
    "Morfosintaxis de la Interjección",
    "Morfosintaxis de los Adverbios",
    "Morfosintaxis de las Preposiciones",
    "Morfosintaxis de las Conjunciones",
    "Morfosintaxis de los Artículos",
    "Morfosintaxis de los Demostrativos y Posesivos",
    "Morfosintaxis de los Indefinidos y Numerales",
    "Morfosintaxis de los Relativos",
    "Morfosintaxis de los Interrogativos y Exclamativos",
    "Morfosintaxis de los Verbos Regulares e Irregulares",
    "Morfosintaxis de los Verbos Auxiliares",
    "Morfosintaxis de los Verbos Copulativos",
    "Morfosintaxis de los Verbos Transitivos e Intransitivos",
    "Morfosintaxis de los Verbos Pronominales",
    "Morfosintaxis de los Verbos Defectivos",
    "Morfosintaxis de los Verbos Impersonales",
    "Morfosintaxis de los Verbos en Formas No Personales",
    "Morfosintaxis del Infinitivo",
    "Morfosintaxis del Gerundio",
    "Morfosintaxis del Participio",
    "Morfosintaxis de los Sustantivos: Género y Número",
    "Morfosintaxis de los Adjetivos: Grados y Funciones",
    "Morfosintaxis de los Adjetivos Determinativos",
    "Morfosintaxis de los Adjetivos Calificativos",
    "Morfosintaxis de los Pronombres Personales",
    "Morfosintaxis de los Pronombres Reflexivos",
    "Morfosintaxis de los Pronombres Recíprocos",
    "Morfosintaxis de los Pronombres Posesivos",
    "Morfosintaxis de los Pronombres Demostrativos",
    "Morfosintaxis de los Pronombres Indefinidos",
    "Morfosintaxis de los Pronombres Numerales",
    "Morfosintaxis de los Pronombres Interrogativos",
    "Morfosintaxis de los Pronombres Exclamativos",
    "Morfosintaxis de los Sintagmas Nominales",
    "Morfosintaxis de los Sintagmas Verbales",
    "Morfosintaxis de los Sintagmas Adjetivales",
    "Morfosintaxis de los Sintagmas Adverbiales",
    "Morfosintaxis de los Sintagmas Preposicionales",
    "Morfosintaxis de los Complementos del Nombre",
    "Morfosintaxis de los Complementos del Adjetivo",
    "Morfosintaxis de los Complementos del Adverbio",
    "Morfosintaxis de la Negación",
    "Morfosintaxis de la Afirmación",
    "Morfosintaxis de la Modalidad Oracional",
    "Morfosintaxis de la Temporalidad",
    "Morfosintaxis de la Aspectualidad",
    "Morfosintaxis de la Voz Media",
    "Morfosintaxis de la Ergatividad",
    "Morfosintaxis de la Transitividad",
    "Morfosintaxis de la Intransitividad",
    "Morfosintaxis de la Impersonalidad",
    "Morfosintaxis de la Pasiva Refleja",
    "Morfosintaxis de la Oración Interrogativa Indirecta",
    "Morfosintaxis de la Oración Exclamativa Indirecta",
    "Morfosintaxis de la Oración Desiderativa Indirecta",
    "Morfosintaxis de la Oración Dubitativa Indirecta",
    "Morfosintaxis de la Oración Optativa Indirecta",
    "Morfosintaxis de la Oración de Relativo",
    "Morfosintaxis de la Oración de Infinitivo",
    "Morfosintaxis de la Oración de Gerundio",
    "Morfosintaxis de la Oración de Participio",
    "Morfosintaxis: Análisis Integral de la Oración",
]

# Temas para lecciones
TEMAS_LECCION = [
    "Introducción al Tema",
    "Conceptos Fundamentales",
    "Análisis Morfológico",
    "Análisis Sintáctico",
    "Estructura de la Oración",
    "Clasificación de Palabras",
    "Funciones Sintácticas",
    "Concordancia",
    "Régimen Verbal",
    "Complementos Verbales",
    "Subordinación",
    "Coordinación",
    "Yuxtaposición",
    "Casos Prácticos",
    "Ejercicios de Aplicación",
]

# Niveles
NIVELES = ["Básico", "Intermedio", "Avanzado"]

# Categoría fija
CATEGORIA = "Morfosintaxis Castellana"

# ============================================================
# 4. GENERAR CURSOS
# ============================================================

cursos_creados = 0
lecciones_creadas = 0
ejercicios_creados = 0

# Tomar solo 100 títulos (si hay más, seleccionar aleatoriamente)
titulos_seleccionados = random.sample(TITULOS_CURSOS, min(100, len(TITULOS_CURSOS)))

for idx, titulo in enumerate(titulos_seleccionados, 1):
    print(f"\n📚 [{idx}/100] Creando curso: {titulo[:50]}...")
    
    nivel = random.choice(NIVELES)
    descripcion = f"Curso completo sobre {titulo.lower()}. Aprende los fundamentos y aplicaciones de la morfosintaxis castellana."

    # Crear curso
    curso = Curso.objects.create(
        titulo=titulo,
        descripcion=descripcion,
        categoria=CATEGORIA,
        nivel=nivel,
    )
    cursos_creados += 1

    # Generar lecciones (entre 3 y 5)
    num_lecciones = random.randint(3, 5)
    temas = random.sample(TEMAS_LECCION, min(num_lecciones, len(TEMAS_LECCION)))
    
    for i, tema in enumerate(temas, 1):
        leccion = Leccion.objects.create(
            curso=curso,
            orden=i,
            titulo=f"Lección {i}: {tema}",
            descripcion=f"En esta lección exploramos {tema.lower()} aplicado a la morfosintaxis castellana."
        )
        lecciones_creadas += 1

        # Generar ejercicios (entre 3 y 6)
        num_ejercicios = random.randint(3, 6)
        for j in range(num_ejercicios):
            tipo = random.choice(['OPCION_MULTIPLE', 'VERDADERO_FALSO', 'TEXTO'])
            
            if tipo == 'OPCION_MULTIPLE':
                pregunta = f"Ejercicio {j+1}: ¿Cuál es la función sintáctica del sintagma destacado en la oración: 'El niño come una manzana'?"
                opciones = ['Sujeto', 'Complemento Directo', 'Complemento Indirecto', 'Complemento Circunstancial']
                respuesta = 'Complemento Directo'
                explicacion = "El sintagma 'una manzana' cumple la función de Complemento Directo."
            
            elif tipo == 'VERDADERO_FALSO':
                pregunta = f"Ejercicio {j+1}: ¿El verbo 'ser' es siempre copulativo?"
                opciones = ['Verdadero', 'Falso']
                respuesta = 'Falso'
                explicacion = "El verbo 'ser' puede ser copulativo o predicativo en ciertos contextos."
            
            else:  # TEXTO
                pregunta = f"Ejercicio {j+1}: Explica la diferencia entre morfología y sintaxis."
                opciones = []
                respuesta = "La morfología estudia la estructura interna de las palabras, mientras que la sintaxis estudia la combinación de palabras para formar oraciones."
                explicacion = "Respuesta de ejemplo."

            ejercicio = Ejercicio.objects.create(
                leccion=leccion,
                titulo=f"Ejercicio {j+1}: {tema[:30]}",
                pregunta=pregunta,
                opciones=opciones,
                respuesta_correcta=respuesta,
                explicacion=explicacion,
                puntos=random.randint(1, 5),
            )
            ejercicios_creados += 1

        print(f"    📖 Lección {i}/{num_lecciones}: {leccion.titulo[:40]} - {num_ejercicios} ejercicios")

# ============================================================
# 5. ESTADÍSTICAS FINALES
# ============================================================

print("\n" + "=" * 70)
print("📊 RESUMEN FINAL")
print("=" * 70)
print(f"   📚 Cursos creados: {cursos_creados}")
print(f"   📖 Lecciones creadas: {lecciones_creadas}")
print(f"   📝 Ejercicios creados: {ejercicios_creados}")
print("=" * 70)
print("✅ ¡CONTENIDO GENERADO EXITOSAMENTE!")

# Verificar totales actuales
total_cursos_actual = Curso.objects.count()
total_lecciones_actual = Leccion.objects.count()
total_ejercicios_actual = Ejercicio.objects.count()

print(f"\n📊 Totales actuales en la base de datos:")
print(f"   Cursos: {total_cursos_actual}")
print(f"   Lecciones: {total_lecciones_actual}")
print(f"   Ejercicios: {total_ejercicios_actual}")
