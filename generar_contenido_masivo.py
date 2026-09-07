#!/usr/bin/env python3
"""
Script para generar contenido masivo en Linguakit-Academy
- 50 Programas (apps.core.models.Programa)
- Cursos (apps.content.models.Curso) - campos: titulo, descripcion, categoria, nivel
- Lecciones (apps.content.models.Leccion) - campos: curso, orden, titulo, descripcion
- Ejercicios (apps.content.models.Ejercicio) - campos: leccion, titulo, pregunta, opciones, respuesta_correcta, explicacion, puntos
"""

import os
import sys
import random
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linguakit.settings')
import django
django.setup()

from django.contrib.auth import get_user_model
from apps.core.models import Programa
from apps.content.models import Curso, Leccion, Ejercicio

User = get_user_model()

print("=" * 60)
print("🚀 GENERANDO CONTENIDO MASIVO - 50 PROGRAMAS")
print("=" * 60)

# ============================================================
# 1. 50 PROGRAMAS (si ya existen, no se duplican)
# ============================================================

PROGRAMAS = [
    {"nombre": "Lengua Castellana", "descripcion": "Gramática, sintaxis, ortografía y redacción."},
    {"nombre": "Literatura Hispanoamericana", "descripcion": "Autores y obras de Latinoamérica."},
    {"nombre": "Literatura Española", "descripcion": "Grandes autores de España."},
    {"nombre": "Poesía Universal", "descripcion": "Análisis de poemas y corrientes poéticas."},
    {"nombre": "Narrativa Contemporánea", "descripcion": "Tendencias actuales de la narrativa."},
    {"nombre": "Teatro y Dramaturgia", "descripcion": "Análisis de obras teatrales."},
    {"nombre": "Ensayo y Crítica", "descripcion": "Género ensayístico y crítica literaria."},
    {"nombre": "Lingüística General", "descripcion": "Estudio científico del lenguaje."},
    {"nombre": "Fonética y Fonología", "descripcion": "Sonidos del lenguaje."},
    {"nombre": "Morfología", "descripcion": "Estructura de las palabras."},
    {"nombre": "Sintaxis", "descripcion": "Estructura de las oraciones."},
    {"nombre": "Semántica", "descripcion": "Significado de las palabras."},
    {"nombre": "Pragmática", "descripcion": "Uso del lenguaje en contexto."},
    {"nombre": "Sociolingüística", "descripcion": "Relación entre lenguaje y sociedad."},
    {"nombre": "Psicolingüística", "descripcion": "Procesos mentales del lenguaje."},
    {"nombre": "Redacción Académica", "descripcion": "Escritura de trabajos académicos."},
    {"nombre": "Redacción Periodística", "descripcion": "Escritura de noticias y reportajes."},
    {"nombre": "Redacción Creativa", "descripcion": "Técnicas de escritura literaria."},
    {"nombre": "Redacción Científica", "descripcion": "Escritura de artículos científicos."},
    {"nombre": "Comunicación Oral", "descripcion": "Hablar en público y oratoria."},
    {"nombre": "Comunicación Digital", "descripcion": "Redacción para medios digitales."},
    {"nombre": "Comunicación Corporativa", "descripcion": "Comunicación en empresas."},
    {"nombre": "Inglés Básico", "descripcion": "Fundamentos del inglés."},
    {"nombre": "Inglés Intermedio", "descripcion": "Nivel intermedio de inglés."},
    {"nombre": "Inglés Avanzado", "descripcion": "Nivel avanzado de inglés."},
    {"nombre": "Francés Básico", "descripcion": "Primeros pasos en francés."},
    {"nombre": "Francés Intermedio", "descripcion": "Nivel intermedio de francés."},
    {"nombre": "Alemán Básico", "descripcion": "Fundamentos del alemán."},
    {"nombre": "Portugués Básico", "descripcion": "Fundamentos del portugués."},
    {"nombre": "Italiano Básico", "descripcion": "Fundamentos del italiano."},
    {"nombre": "Chino Mandarín Básico", "descripcion": "Fundamentos del chino."},
    {"nombre": "Historia Universal", "descripcion": "Historia de la humanidad."},
    {"nombre": "Historia de América", "descripcion": "Historia del continente americano."},
    {"nombre": "Geografía", "descripcion": "Estudio de la tierra y sus habitantes."},
    {"nombre": "Filosofía", "descripcion": "Reflexión sobre el pensamiento y la existencia."},
    {"nombre": "Ética y Valores", "descripcion": "Reflexión sobre la moral y los valores."},
    {"nombre": "Psicología", "descripcion": "Estudio de la mente y el comportamiento."},
    {"nombre": "Sociología", "descripcion": "Estudio de la sociedad y sus estructuras."},
    {"nombre": "Antropología", "descripcion": "Estudio de las culturas humanas."},
    {"nombre": "Biología General", "descripcion": "Estudio de los seres vivos."},
    {"nombre": "Química General", "descripcion": "Estudio de la materia y sus transformaciones."},
    {"nombre": "Física General", "descripcion": "Estudio de la energía y la materia."},
    {"nombre": "Astronomía", "descripcion": "Estudio del universo."},
    {"nombre": "Ecología", "descripcion": "Estudio de los ecosistemas."},
    {"nombre": "Matemáticas Básicas", "descripcion": "Fundamentos de matemáticas."},
    {"nombre": "Álgebra", "descripcion": "Ecuaciones y funciones."},
    {"nombre": "Geometría", "descripcion": "Formas y espacios."},
    {"nombre": "Estadística", "descripcion": "Análisis de datos."},
    {"nombre": "Programación Básica", "descripcion": "Fundamentos de programación."},
    {"nombre": "Desarrollo Web", "descripcion": "Creación de sitios y aplicaciones web."},
    {"nombre": "Bases de Datos", "descripcion": "Diseño y gestión de bases de datos."},
]

def crear_programas():
    creados = 0
    for data in PROGRAMAS:
        programa, created = Programa.objects.get_or_create(
            nombre=data['nombre'],
            defaults={'descripcion': data['descripcion']}
        )
        if created:
            creados += 1
            print(f"  📁 Programa: {programa.nombre}")
    return creados

# ============================================================
# 2. CURSOS (sin relación directa con Programa)
# ============================================================

def generar_cursos_para_programa(nombre_programa, cantidad=3):
    prefijos = ["Introducción a", "Fundamentos de", "Práctica de", "Técnicas de", "Avanzado en"]
    sufijos = ["Básico", "Intermedio", "Avanzado", "Práctico", "Teórico"]
    niveles = ["Básico", "Intermedio", "Avanzado"]
    
    cursos = []
    palabras = nombre_programa.split()
    tema = random.choice(palabras) if palabras else nombre_programa
    for i in range(cantidad):
        prefijo = random.choice(prefijos)
        sufijo = random.choice(sufijos)
        titulo = f"{prefijo} {tema} {sufijo}"
        if len(titulo) > 80:
            titulo = titulo[:80]
        cursos.append({
            "titulo": titulo,
            "descripcion": f"Curso sobre {tema} dentro del programa {nombre_programa}.",
            "categoria": nombre_programa,
            "nivel": random.choice(niveles),
        })
    return cursos

def crear_cursos():
    creados = 0
    programas = Programa.objects.all()
    for programa in programas:
        num_cursos = random.randint(2, 4)
        cursos_data = generar_cursos_para_programa(programa.nombre, num_cursos)
        for curso_data in cursos_data:
            curso, created = Curso.objects.get_or_create(
                titulo=curso_data['titulo'],
                defaults={
                    'descripcion': curso_data['descripcion'],
                    'categoria': curso_data['categoria'],
                    'nivel': curso_data['nivel'],
                }
            )
            if created:
                creados += 1
                print(f"    📚 Curso: {curso.titulo} (categoría: {curso.categoria})")
    return creados

# ============================================================
# 3. LECCIONES (sin contenido)
# ============================================================

def crear_lecciones():
    temas = [
        "Introducción", "Conceptos Básicos", "Fundamentos", "Estructura",
        "Análisis", "Práctica", "Ejercicios", "Evaluación",
        "Aplicación", "Proyecto", "Caso de Estudio", "Profundización",
        "Técnicas Avanzadas", "Optimización", "Recursos Adicionales"
    ]
    creados = 0
    cursos = Curso.objects.all()
    for curso in cursos:
        num_lecciones = random.randint(3, 6)
        temas_sel = random.sample(temas, min(num_lecciones, len(temas)))
        for i, tema in enumerate(temas_sel, 1):
            leccion, created = Leccion.objects.get_or_create(
                curso=curso,
                orden=i,
                defaults={
                    'titulo': f"Lección {i}: {tema}",
                    'descripcion': f"Lección sobre {tema} para {curso.titulo}",
                }
            )
            if created:
                creados += 1
        print(f"    📖 Curso: {curso.titulo} - {len(temas_sel)} lecciones")
    return creados

# ============================================================
# 4. EJERCICIOS (vinculados a lecciones)
# ============================================================

def generar_ejercicios():
    tipos = ['OPCION_MULTIPLE', 'VERDADERO_FALSO', 'TEXTO', 'RELACIONAR', 'ORDENAR']
    creados = 0
    lecciones = Leccion.objects.all()
    for leccion in lecciones:
        num_ejercicios = random.randint(3, 6)
        for i in range(num_ejercicios):
            tipo = random.choice(tipos)
            if tipo == 'OPCION_MULTIPLE':
                pregunta = f"Pregunta {i+1}: ¿Cuál es el concepto de {leccion.titulo[:30]}?"
                opciones = ['Opción A', 'Opción B', 'Opción C', 'Opción D']
                respuesta = 'Opción A'
                explicacion = f"La respuesta correcta es Opción A porque..."
            elif tipo == 'VERDADERO_FALSO':
                pregunta = f"Pregunta {i+1}: ¿Es correcto que {leccion.titulo[:30]} es fundamental?"
                opciones = ['Verdadero', 'Falso']
                respuesta = 'Verdadero'
                explicacion = "Es correcto porque..."
            elif tipo == 'TEXTO':
                pregunta = f"Pregunta {i+1}: Explica el concepto de {leccion.titulo[:30]}"
                opciones = []
                respuesta = 'Respuesta modelo'
                explicacion = "Esta es una respuesta de ejemplo."
            else:
                pregunta = f"Pregunta {i+1}: Relaciona los conceptos de {leccion.titulo[:30]}"
                opciones = []
                respuesta = 'A-1, B-2'
                explicacion = "La relación correcta es A-1, B-2."

            ejercicio, created = Ejercicio.objects.get_or_create(
                leccion=leccion,
                pregunta=pregunta,
                defaults={
                    'titulo': f"Ejercicio {i+1}: {leccion.titulo[:30]}",
                    'opciones': opciones,
                    'respuesta_correcta': respuesta,
                    'explicacion': explicacion,
                    'puntos': random.randint(1, 5),
                }
            )
            if created:
                creados += 1
        print(f"    📝 Lección: {leccion.titulo[:40]} - {num_ejercicios} ejercicios")
    return creados

# ============================================================
# 5. EJECUCIÓN
# ============================================================

def main():
    print("\n📁 1. Creando 50 Programas...")
    programas_creados = crear_programas()
    print(f"   ✅ {programas_creados} programas creados")
    total_programas = Programa.objects.count()
    print(f"   📊 Total programas: {total_programas}")

    print("\n📚 2. Creando Cursos...")
    cursos_creados = crear_cursos()
    print(f"   ✅ {cursos_creados} cursos creados")
    total_cursos = Curso.objects.count()
    print(f"   📊 Total cursos: {total_cursos}")

    print("\n📖 3. Creando Lecciones...")
    lecciones_creadas = crear_lecciones()
    print(f"   ✅ {lecciones_creadas} lecciones creadas")
    total_lecciones = Leccion.objects.count()
    print(f"   📊 Total lecciones: {total_lecciones}")

    print("\n📝 4. Creando Ejercicios...")
    ejercicios_creados = generar_ejercicios()
    print(f"   ✅ {ejercicios_creados} ejercicios creados")
    total_ejercicios = Ejercicio.objects.count()
    print(f"   📊 Total ejercicios: {total_ejercicios}")

    print("\n" + "=" * 60)
    print("📊 RESUMEN FINAL")
    print("=" * 60)
    print(f"   📁 Programas: {total_programas}")
    print(f"   📚 Cursos: {total_cursos}")
    print(f"   📖 Lecciones: {total_lecciones}")
    print(f"   📝 Ejercicios: {total_ejercicios}")
    print("=" * 60)
    print("✅ ¡CONTENIDO GENERADO EXITOSAMENTE!")

if __name__ == "__main__":
    main()
