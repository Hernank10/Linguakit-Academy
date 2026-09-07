import random
import re
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.content.models import LinguisticTechnique, Curso, Leccion, Ejercicio, Evaluacion

class Command(BaseCommand):
    help = 'Genera cursos, lecciones, prácticas y evaluaciones a partir de técnicas'

    def add_arguments(self, parser):
        parser.add_argument('--num-cursos', type=int, default=10)
        parser.add_argument('--tecnicas-por-leccion', type=int, default=5)

    @transaction.atomic
    def handle(self, *args, **options):
        num_cursos = min(options['num_cursos'], 50)
        tecnicas_por_leccion = options['tecnicas_por_leccion']
        tecnicas = list(LinguisticTechnique.objects.all())
        if not tecnicas:
            self.stdout.write(self.style.ERROR('❌ No hay técnicas'))
            return

        self.stdout.write(f'📚 {len(tecnicas)} técnicas disponibles')

        # Agrupar por categoría
        agrupadas = {}
        for t in tecnicas:
            cat = t.category or 'Sin categoría'
            agrupadas.setdefault(cat, []).append(t)

        # Seleccionar categorías con más técnicas
        categorias_seleccionadas = sorted(
            agrupadas.items(), key=lambda x: len(x[1]), reverse=True
        )[:num_cursos]

        for categoria, tecnicas_cat in categorias_seleccionadas:
            curso = self._crear_curso(categoria, tecnicas_cat)
            self.stdout.write(f'✅ Curso: {curso.titulo}')

            lecciones = self._crear_lecciones(curso, tecnicas_cat, tecnicas_por_leccion)
            self.stdout.write(f'   📖 {len(lecciones)} lecciones')

            for leccion in lecciones:
                ejercicios = self._crear_ejercicios(leccion)
                self.stdout.write(f'   📝 {len(ejercicios)} ejercicios en "{leccion.titulo}"')

            evaluacion = self._crear_evaluacion(curso, tecnicas_cat)
            if evaluacion:
                self.stdout.write(f'   📊 Evaluación: {evaluacion.titulo}')

        self.stdout.write(self.style.SUCCESS('\n🎉 Generación completada'))

    def _crear_curso(self, categoria, tecnicas):
        titulo = f"Curso de {categoria.capitalize()}"
        descripcion = f"Curso completo sobre {categoria}. {len(tecnicas)} técnicas."
        niveles = [t.level for t in tecnicas if t.level]
        nivel = max(set(niveles), key=niveles.count) if niveles else 'B1'
        curso, _ = Curso.objects.get_or_create(
            titulo=titulo,
            defaults={'descripcion': descripcion, 'categoria': categoria, 'nivel': nivel}
        )
        return curso

    def _crear_lecciones(self, curso, tecnicas, tamano):
        lecciones = []
        random.shuffle(tecnicas)
        for i in range(0, len(tecnicas), tamano):
            grupo = tecnicas[i:i+tamano]
            if not grupo:
                continue
            titulo = f"Lección {i//tamano+1}: {grupo[0].title[:50]}"
            descripcion = " | ".join([t.theory[:100] for t in grupo if t.theory])[:500]
            leccion, _ = Leccion.objects.get_or_create(
                curso=curso,
                titulo=titulo,
                defaults={'descripcion': descripcion, 'orden': i//tamano+1}
            )
            lecciones.append(leccion)
        return lecciones

    def _crear_ejercicios(self, leccion):
        ejercicios = []
        # Tomar técnicas de la categoría del curso
        tecnicas_cat = LinguisticTechnique.objects.filter(category=leccion.curso.categoria)
        seleccionadas = random.sample(list(tecnicas_cat), min(3, tecnicas_cat.count()))
        for t in seleccionadas:
            pregunta = t.exercise_text or t.theory[:200]
            respuesta = t.correct_answer or "Revisa la teoría"
            opciones = self._generar_opciones(t, tecnicas_cat)
            ejercicio, _ = Ejercicio.objects.get_or_create(
                leccion=leccion,
                titulo=f"Práctica: {t.title[:40]}",
                defaults={
                    'pregunta': pregunta,
                    'opciones': opciones,
                    'respuesta_correcta': respuesta,
                    'explicacion': t.theory[:300] if t.theory else '',
                    'puntos': random.randint(5, 15)
                }
            )
            ejercicios.append(ejercicio)
        return ejercicios

    def _generar_opciones(self, tecnica, todas):
        opciones = []
        if tecnica.correct_answer:
            opciones.append(tecnica.correct_answer)
            otras = [t.correct_answer for t in todas if t.correct_answer and t.id != tecnica.id]
            random.shuffle(otras)
            distractores = otras[:3]
            while len(distractores) < 3:
                distractores.append("Respuesta incorrecta")
            opciones.extend(distractores)
            random.shuffle(opciones)
        return opciones

    def _crear_evaluacion(self, curso, tecnicas):
        if len(tecnicas) < 5:
            return None
        seleccionadas = random.sample(tecnicas, min(10, len(tecnicas)))
        preguntas = []
        for t in seleccionadas:
            texto = t.theory or t.exercise_text
            if not texto:
                continue
            frase = re.sub(r'\s+', ' ', texto.strip())[:200]
            opciones = self._generar_opciones(t, tecnicas)
            preguntas.append({
                'pregunta': f"Según '{t.title}', ¿qué es correcto?",
                'texto_base': frase,
                'opciones': opciones,
                'respuesta': t.correct_answer or "Revisa la técnica",
                'explicacion': t.theory[:200] if t.theory else ''
            })
        if not preguntas:
            return None
        evaluacion, _ = Evaluacion.objects.get_or_create(
            curso=curso,
            titulo=f"Evaluación de {curso.titulo}",
            defaults={
                'descripcion': f"Evalúa tu conocimiento sobre {curso.categoria}",
                'preguntas': preguntas,
                'puntaje_total': len(preguntas) * 10
            }
        )
        return evaluacion
