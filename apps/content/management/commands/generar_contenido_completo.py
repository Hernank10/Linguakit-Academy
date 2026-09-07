import random
import re
import json
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count, Q
from apps.content.models import (
    LinguisticTechnique, 
    Curso, 
    Leccion, 
    Ejercicio, 
    Evaluacion
)
from apps.usuarios.models import Usuario

class Command(BaseCommand):
    help = 'Genera lecciones, 50 ejercicios interactivos por lección y evaluaciones con 100 ejercicios'

    def add_arguments(self, parser):
        parser.add_argument(
            '--num-ejercicios',
            type=int,
            default=50,
            help='Número de ejercicios por lección (por defecto 50)'
        )
        parser.add_argument(
            '--num-evaluacion',
            type=int,
            default=100,
            help='Número de preguntas por evaluación (por defecto 100)'
        )
        parser.add_argument(
            '--cursos',
            type=str,
            help='IDs de cursos específicos separados por coma (ej: 1,2,3)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Eliminar lecciones, ejercicios y evaluaciones existentes'
        )
        parser.add_argument(
            '--tecnicas-por-leccion',
            type=int,
            default=10,
            help='Técnicas base por lección (para generar contenido variado)'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        num_ejercicios = options['num_ejercicios']
        num_evaluacion = options['num_evaluacion']
        cursos_ids = options.get('cursos')
        clear = options['clear']
        tecnicas_por_leccion = options['tecnicas_por_leccion']

        # Obtener cursos a procesar
        if cursos_ids:
            curso_ids = [int(x.strip()) for x in cursos_ids.split(',')]
            cursos = Curso.objects.filter(id__in=curso_ids)
            self.stdout.write(f'📚 Procesando {len(cursos)} cursos específicos')
        else:
            cursos = Curso.objects.all()
            self.stdout.write(f'📚 Procesando todos los cursos ({cursos.count()})')

        if not cursos.exists():
            self.stdout.write(self.style.ERROR('❌ No hay cursos disponibles'))
            return

        # Si clear, eliminar datos existentes (lecciones, ejercicios, evaluaciones)
        if clear:
            lecciones_eliminadas = Leccion.objects.filter(curso__in=cursos).delete()
            ejercicios_eliminados = Ejercicio.objects.filter(leccion__curso__in=cursos).delete()
            evaluaciones_eliminadas = Evaluacion.objects.filter(curso__in=cursos).delete()
            self.stdout.write('🗑️ Datos anteriores eliminados')

        # Cargar todas las técnicas
        todas_tecnicas = list(LinguisticTechnique.objects.all())
        self.stdout.write(f'📊 Técnicas disponibles: {len(todas_tecnicas)}')

        if not todas_tecnicas:
            self.stdout.write(self.style.ERROR('❌ No hay técnicas importadas'))
            return

        total_lecciones = 0
        total_ejercicios = 0
        total_evaluaciones = 0

        for curso in cursos:
            self.stdout.write(f'\n🎓 Procesando curso: {curso.titulo}')

            # 1. Generar lecciones para el curso
            lecciones = self._generar_lecciones(curso, todas_tecnicas, tecnicas_por_leccion)
            self.stdout.write(f'   📖 {len(lecciones)} lecciones generadas')

            # 2. Para cada lección, generar 50 ejercicios interactivos
            for leccion in lecciones:
                ejercicios = self._generar_ejercicios_leccion(leccion, todas_tecnicas, num_ejercicios)
                total_ejercicios += len(ejercicios)
                self.stdout.write(f'      📝 {len(ejercicios)} ejercicios en "{leccion.titulo[:30]}"')

            # 3. Generar evaluación con 100 ejercicios para el curso
            evaluacion = self._generar_evaluacion(curso, todas_tecnicas, num_evaluacion)
            if evaluacion:
                total_evaluaciones += 1
                self.stdout.write(f'   📊 Evaluación generada: {evaluacion.titulo} ({len(evaluacion.preguntas)} preguntas)')

            total_lecciones += len(lecciones)

        self.stdout.write(self.style.SUCCESS(f'\n🎉 GENERACIÓN COMPLETADA'))
        self.stdout.write(f'   📚 Lecciones: {total_lecciones}')
        self.stdout.write(f'   📝 Ejercicios: {total_ejercicios}')
        self.stdout.write(f'   📊 Evaluaciones: {total_evaluaciones}')

    def _generar_lecciones(self, curso, tecnicas, tecnicas_por_leccion):
        """Genera lecciones basadas en técnicas de la misma categoría del curso"""
        # Filtrar técnicas que coincidan con la categoría del curso
        tecnicas_curso = [t for t in tecnicas if t.category and t.category.lower() in curso.categoria.lower()]
        
        # Si no hay suficientes, usar todas
        if len(tecnicas_curso) < 5:
            tecnicas_curso = tecnicas[:100]  # Usar un subconjunto

        random.shuffle(tecnicas_curso)
        lecciones = []

        # Crear lecciones agrupando técnicas
        for i in range(0, min(len(tecnicas_curso), 100), tecnicas_por_leccion):
            grupo = tecnicas_curso[i:i+tecnicas_por_leccion]
            if len(grupo) < 3:
                continue

            titulo_base = grupo[0].title if grupo[0].title else "Lección"
            titulo = f"Lección {i//tecnicas_por_leccion + 1}: {titulo_base[:40]}"
            
            descripcion = " | ".join([t.theory[:80] for t in grupo if t.theory])[:500]
            
            leccion, creado = Leccion.objects.get_or_create(
                curso=curso,
                titulo=titulo,
                defaults={
                    'descripcion': descripcion,
                    'orden': i//tecnicas_por_leccion + 1
                }
            )
            lecciones.append(leccion)

        return lecciones

    def _generar_ejercicios_leccion(self, leccion, tecnicas, cantidad):
        """Genera ejercicios interactivos para una lección"""
        ejercicios = []
        
        # Usar técnicas de la misma categoría del curso
        tecnicas_cat = [t for t in tecnicas if t.category and t.category.lower() in leccion.curso.categoria.lower()]
        if len(tecnicas_cat) < 10:
            tecnicas_cat = tecnicas[:200]

        # Seleccionar técnicas para ejercicios
        seleccionadas = random.sample(tecnicas_cat, min(cantidad, len(tecnicas_cat)))

        for idx, t in enumerate(seleccionadas):
            # Construir pregunta variada
            pregunta = self._generar_pregunta(t)
            opciones = self._generar_opciones(t, tecnicas_cat)
            respuesta_correcta = t.correct_answer or "Revisa la teoría"
            
            ejercicio, _ = Ejercicio.objects.get_or_create(
                leccion=leccion,
                titulo=f"Ejercicio {idx+1}: {t.title[:30]}",
                defaults={
                    'pregunta': pregunta,
                    'opciones': opciones,
                    'respuesta_correcta': respuesta_correcta,
                    'explicacion': t.theory[:300] if t.theory else 'Sin explicación disponible',
                    'puntos': random.randint(5, 20)
                }
            )
            ejercicios.append(ejercicio)

        return ejercicios

    def _generar_pregunta(self, tecnica):
        """Genera una pregunta variada a partir de una técnica"""
        templates = [
            f"Según la técnica '{tecnica.title}', ¿cuál de las siguientes afirmaciones es correcta?",
            f"Basado en el concepto de '{tecnica.title}', selecciona la opción correcta:",
            f"¿Qué se afirma en la técnica '{tecnica.title}' sobre el tema tratado?",
            f"De acuerdo con '{tecnica.title}', ¿qué enunciado es verdadero?",
            f"En relación a '{tecnica.title}', identifica la opción correcta:"
        ]
        return random.choice(templates)

    def _generar_opciones(self, tecnica, todas):
        """Genera opciones múltiples con distractores"""
        opciones = []
        
        # Siempre incluir la respuesta correcta (si existe)
        if tecnica.correct_answer:
            opciones.append(tecnica.correct_answer)
        else:
            # Si no tiene, usar el título como base
            opciones.append(tecnica.title)

        # Obtener distractores de otras técnicas
        otras_respuestas = [t.correct_answer for t in todas if t.correct_answer and t.id != tecnica.id]
        random.shuffle(otras_respuestas)
        distractores = otras_respuestas[:3]
        
        # Si no hay suficientes distractores, generar algunos genéricos
        while len(distractores) < 3:
            distractores.append(f"Opción incorrecta {len(distractores)+1}")

        opciones.extend(distractores)
        random.shuffle(opciones)
        return opciones

    def _generar_evaluacion(self, curso, tecnicas, cantidad):
        """Genera una evaluación con preguntas tipo test para el curso"""
        # Seleccionar técnicas de la categoría del curso
        tecnicas_cat = [t for t in tecnicas if t.category and t.category.lower() in curso.categoria.lower()]
        if len(tecnicas_cat) < 20:
            tecnicas_cat = tecnicas[:300]

        if len(tecnicas_cat) < cantidad:
            cantidad = len(tecnicas_cat)

        seleccionadas = random.sample(tecnicas_cat, min(cantidad, len(tecnicas_cat)))
        preguntas = []

        for t in seleccionadas:
            texto_base = t.theory or t.exercise_text
            if not texto_base:
                texto_base = t.title
            
            # Generar pregunta
            pregunta_texto = self._generar_pregunta(t)
            opciones = self._generar_opciones(t, tecnicas_cat)
            
            preguntas.append({
                'pregunta': pregunta_texto,
                'texto_base': texto_base[:200],
                'opciones': opciones,
                'respuesta': t.correct_answer or "Revisa la técnica",
                'explicacion': t.theory[:200] if t.theory else 'Sin explicación'
            })

        if not preguntas:
            return None

        evaluacion, _ = Evaluacion.objects.get_or_create(
            curso=curso,
            titulo=f"Evaluación Final: {curso.titulo}",
            defaults={
                'descripcion': f"Evalúa tus conocimientos sobre {curso.categoria}. Contiene {len(preguntas)} preguntas.",
                'preguntas': preguntas,
                'puntaje_total': len(preguntas) * 10
            }
        )
        return evaluacion
