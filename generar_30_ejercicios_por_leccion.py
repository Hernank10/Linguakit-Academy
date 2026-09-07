#!/usr/bin/env python3
"""
Script para generar al menos 30 ejercicios por cada lección existente.
Si una lección ya tiene 30 o más, se omite.
Si tiene menos, se generan los suficientes para llegar a 30.
"""

import os
import sys
import random
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linguakit.settings')
import django
django.setup()

from apps.content.models import Leccion, Ejercicio

print("=" * 70)
print("📝 GENERANDO 30 EJERCICIOS POR LECCIÓN")
print("=" * 70)

# ============================================================
# 1. DEFINIR TEMAS Y TIPOS DE EJERCICIOS
# ============================================================

TEMAS = [
    "morfosintaxis", "gramática", "sintaxis", "morfología",
    "análisis sintáctico", "categorías gramaticales", "concordancia",
    "régimen verbal", "complementos", "subordinación", "coordinación",
    "yuxtaposición", "voz activa", "voz pasiva", "perífrasis"
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

# ============================================================
# 2. PROCESAR CADA LECCIÓN
# ============================================================

lecciones = Leccion.objects.all()
total_lecciones = lecciones.count()
print(f"\n📖 Lecciones encontradas: {total_lecciones}")

ejercicios_generados = 0
lecciones_completadas = 0
lecciones_omitidas = 0

for idx, leccion in enumerate(lecciones, 1):
    # Contar ejercicios actuales
    count = Ejercicio.objects.filter(leccion=leccion).count()
    
    if count >= 30:
        print(f"  [{idx}/{total_lecciones}] ✅ {leccion.titulo[:40]} - ya tiene {count} ejercicios (suficiente)")
        lecciones_omitidas += 1
        continue

    # Cuántos faltan
    faltan = 30 - count
    print(f"  [{idx}/{total_lecciones}] 📝 {leccion.titulo[:40]} - tiene {count}, faltan {faltan}")

    # Generar ejercicios faltantes
    for i in range(faltan):
        tipo = random.choice(TIPOS)
        tema = random.choice(TEMAS)
        data = generar_pregunta(tipo, tema)

        # Crear el ejercicio
        ejercicio = Ejercicio.objects.create(
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

# ============================================================
# 3. ESTADÍSTICAS FINALES
# ============================================================
print("\n" + "=" * 70)
print("📊 ESTADÍSTICAS FINALES")
print("=" * 70)
print(f"   📖 Lecciones procesadas: {total_lecciones}")
print(f"   ✅ Lecciones ya completas (≥30): {lecciones_omitidas}")
print(f"   📝 Lecciones actualizadas: {lecciones_completadas}")
print(f"   📝 Ejercicios generados: {ejercicios_generados}")
print("=" * 70)

# Verificar total final
total_ejercicios = Ejercicio.objects.count()
print(f"\n📊 Total ejercicios en la base de datos: {total_ejercicios}")

# Verificar lecciones con menos de 30 (por si acaso)
lecciones_con_menos = Leccion.objects.annotate(
    count=Count('ejercicios')
).filter(count__lt=30)

if lecciones_con_menos.exists():
    print(f"\n⚠️ Todavía hay {lecciones_con_menos.count()} lecciones con menos de 30 ejercicios.")
    for l in lecciones_con_menos:
        print(f"   - {l.titulo[:40]}: {l.count} ejercicios")
else:
    print("\n✅ ¡TODAS las lecciones tienen al menos 30 ejercicios!")
