#!/usr/bin/env python3
"""
Script para generar ejercicios en lecciones, asegurando un mínimo por lección.
Versión mejorada con importaciones correctas y estadísticas detalladas.
"""

import os
import sys
import random
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linguakit.settings')
import django
django.setup()

from django.db.models import Count
from apps.content.models import Leccion, Ejercicio

# ============================================================
# CONFIGURACIÓN
# ============================================================
MINIMO_EJERCICIOS = 30  # Cambia este número para ajustar el mínimo

TEMAS = [
    "morfosintaxis", "gramática", "sintaxis", "morfología",
    "análisis sintáctico", "categorías gramaticales", "concordancia",
    "régimen verbal", "complementos", "subordinación", "coordinación",
    "yuxtaposición", "voz activa", "voz pasiva", "perífrasis",
    "oraciones subordinadas", "oraciones coordinadas", "sujeto y predicado",
    "complementos del verbo", "adverbios y preposiciones"
]

TIPOS = ['OPCION_MULTIPLE', 'VERDADERO_FALSO', 'TEXTO']

def generar_pregunta(tipo, tema):
    """Genera una pregunta aleatoria del tipo especificado"""
    if tipo == 'OPCION_MULTIPLE':
        return {
            'pregunta': f"¿Cuál es la función sintáctica del sintagma destacado en la oración: 'El niño come una manzana'? (Ejercicio sobre {tema})",
            'opciones': ['Sujeto', 'Complemento Directo', 'Complemento Indirecto', 'Complemento Circunstancial'],
            'respuesta': 'Complemento Directo',
            'explicacion': 'El sintagma "una manzana" cumple la función de Complemento Directo.'
        }
    elif tipo == 'VERDADERO_FALSO':
        return {
            'pregunta': f"¿Es correcto afirmar que '{tema}' es un concepto fundamental en la morfosintaxis?",
            'opciones': ['Verdadero', 'Falso'],
            'respuesta': 'Verdadero',
            'explicacion': f'El concepto de {tema} es fundamental para entender la estructura de las oraciones.'
        }
    else:  # TEXTO
        return {
            'pregunta': f"Explica brevemente el concepto de '{tema}' y da un ejemplo.",
            'opciones': [],
            'respuesta': f'El concepto de {tema} se refiere a... Un ejemplo sería...',
            'explicacion': 'Respuesta de ejemplo.'
        }

def main():
    print("=" * 70)
    print(f"📝 GENERANDO MÍNIMO {MINIMO_EJERCICIOS} EJERCICIOS POR LECCIÓN")
    print("=" * 70)

    lecciones = Leccion.objects.all()
    total_lecciones = lecciones.count()
    print(f"\n📖 Lecciones encontradas: {total_lecciones}")

    ejercicios_generados = 0
    lecciones_completadas = 0
    lecciones_omitidas = 0

    for idx, leccion in enumerate(lecciones, 1):
        count = Ejercicio.objects.filter(leccion=leccion).count()
        
        if count >= MINIMO_EJERCICIOS:
            print(f"  [{idx}/{total_lecciones}] ✅ {leccion.titulo[:40]} - ya tiene {count} ejercicios (suficiente)")
            lecciones_omitidas += 1
            continue

        faltan = MINIMO_EJERCICIOS - count
        print(f"  [{idx}/{total_lecciones}] 📝 {leccion.titulo[:40]} - tiene {count}, faltan {faltan}")

        for i in range(faltan):
            tipo = random.choice(TIPOS)
            tema = random.choice(TEMAS)
            data = generar_pregunta(tipo, tema)

            Ejercicio.objects.create(
                leccion=leccion,
                titulo=f"Ejercicio {count + i + 1}: {tema.capitalize()}",
                pregunta=data['pregunta'],
                opciones=data['opciones'],
                respuesta_correcta=data['respuesta'],
                explicacion=data['explicacion'],
                puntos=random.randint(1, 5),
            )
            ejercicios_generados += 1

        lecciones_completadas += 1

    # Estadísticas finales
    print("\n" + "=" * 70)
    print("📊 ESTADÍSTICAS FINALES")
    print("=" * 70)
    print(f"   📖 Lecciones procesadas: {total_lecciones}")
    print(f"   ✅ Lecciones ya completas (≥{MINIMO_EJERCICIOS}): {lecciones_omitidas}")
    print(f"   📝 Lecciones actualizadas: {lecciones_completadas}")
    print(f"   📝 Ejercicios generados: {ejercicios_generados}")

    total_ejercicios = Ejercicio.objects.count()
    print(f"\n📊 Total ejercicios en la base de datos: {total_ejercicios}")

    # Verificar lecciones con menos del mínimo
    lecciones_con_menos = Leccion.objects.annotate(
        num=Count('ejercicios')
    ).filter(num__lt=MINIMO_EJERCICIOS)

    if lecciones_con_menos.exists():
        print(f"\n⚠️ Todavía hay {lecciones_con_menos.count()} lecciones con menos de {MINIMO_EJERCICIOS} ejercicios.")
        for l in lecciones_con_menos:
            print(f"   - {l.titulo[:40]}: {l.num} ejercicios")
    else:
        print(f"\n✅ ¡TODAS las lecciones tienen al menos {MINIMO_EJERCICIOS} ejercicios!")

if __name__ == "__main__":
    main()
