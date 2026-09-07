import random
import re
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.content.models import LinguisticTechnique, Curso, Evaluacion

class Command(BaseCommand):
    help = 'Asegura que cada curso tenga una evaluación con al menos 100 preguntas'

    def add_arguments(self, parser):
        parser.add_argument('--min-preguntas', type=int, default=100, help='Número mínimo de preguntas por evaluación')
        parser.add_argument('--force', action='store_true', help='Recrear todas las evaluaciones desde cero')

    @transaction.atomic
    def handle(self, *args, **options):
        min_preguntas = options['min_preguntas']
        force = options['force']

        # Obtener todas las técnicas
        tecnicas = list(LinguisticTechnique.objects.all())
        if not tecnicas:
            self.stdout.write(self.style.ERROR('❌ No hay técnicas'))
            return

        # Obtener todos los cursos
        cursos = Curso.objects.all()
        if not cursos:
            self.stdout.write(self.style.ERROR('❌ No hay cursos'))
            return

        self.stdout.write(f'📚 {len(tecnicas)} técnicas disponibles')
        self.stdout.write(f'📂 {len(cursos)} cursos encontrados')

        total_preguntas = 0

        for curso in cursos:
            # Obtener o crear evaluación
            evaluacion, creada = Evaluacion.objects.get_or_create(
                curso=curso,
                defaults={
                    'titulo': f'Evaluación de {curso.titulo}',
                    'descripcion': f'Evalúa tus conocimientos sobre {curso.categoria}.',
                    'preguntas': [],
                    'puntaje_total': 0
                }
            )

            if force or creada or len(evaluacion.preguntas) < min_preguntas:
                # Generar nuevas preguntas
                preguntas_generadas = self._generar_preguntas(curso, tecnicas, min_preguntas)
                evaluacion.preguntas = preguntas_generadas
                evaluacion.puntaje_total = len(preguntas_generadas) * 10
                evaluacion.save()
                total_preguntas += len(preguntas_generadas)
                self.stdout.write(f'✅ {curso.titulo[:40]}: {len(preguntas_generadas)} preguntas')
            else:
                self.stdout.write(f'ℹ️ {curso.titulo[:40]}: ya tiene {len(evaluacion.preguntas)} preguntas')

        self.stdout.write(self.style.SUCCESS(f'\n🎉 Total preguntas generadas: {total_preguntas}'))

    def _generar_preguntas(self, curso, tecnicas, cantidad):
        """Genera preguntas variadas para un curso"""
        # Filtrar técnicas de la categoría del curso
        tecnicas_curso = [t for t in tecnicas if t.category == curso.categoria]
        if not tecnicas_curso:
            tecnicas_curso = tecnicas  # fallback

        # Asegurar suficientes técnicas
        if len(tecnicas_curso) < cantidad:
            tecnicas_curso = tecnicas_curso * (cantidad // len(tecnicas_curso) + 1)
        random.shuffle(tecnicas_curso)

        seleccionadas = tecnicas_curso[:cantidad]
        preguntas = []
        tipos = ['multiple', 'vf', 'completar', 'emparejar']

        for i, t in enumerate(seleccionadas):
            tipo = tipos[i % len(tipos)]
            if tipo == 'multiple':
                pregunta = self._crear_pregunta_multiple(t, tecnicas_curso)
            elif tipo == 'vf':
                pregunta = self._crear_pregunta_vf(t)
            elif tipo == 'completar':
                pregunta = self._crear_pregunta_completar(t)
            else:
                pregunta = self._crear_pregunta_emparejar(t, tecnicas_curso)

            if pregunta:
                preguntas.append(pregunta)

        return preguntas

    def _crear_pregunta_multiple(self, tecnica, todas):
        texto = tecnica.exercise_text or tecnica.theory or ""
        if not texto:
            return None
        pregunta_texto = f"Según la técnica '{tecnica.title}', ¿qué afirmación es correcta?"
        opciones = self._generar_opciones(tecnica, todas)
        if not opciones:
            return None
        return {
            'pregunta': pregunta_texto,
            'texto_base': texto[:200],
            'opciones': opciones,
            'respuesta': tecnica.correct_answer or "Revisa la técnica",
            'tipo': 'multiple',
            'explicacion': tecnica.theory[:300] if tecnica.theory else ''
        }

    def _crear_pregunta_vf(self, tecnica):
        texto = tecnica.theory or tecnica.exercise_text or ""
        if not texto:
            return None
        frases = re.split(r'[.!?]', texto)
        frases = [f.strip() for f in frases if len(f.strip()) > 20]
        if not frases:
            return None
        frase = random.choice(frases)
        es_verdadero = random.choice([True, False])
        if not es_verdadero:
            frase = frase.replace(" es ", " no es ").replace(" son ", " no son ")
        pregunta_texto = f"¿Es correcta la siguiente afirmación?\n\n\"{frase}\""
        return {
            'pregunta': pregunta_texto,
            'texto_base': frase,
            'opciones': ["Verdadero", "Falso"],
            'respuesta': "Verdadero" if es_verdadero else "Falso",
            'tipo': 'vf',
            'explicacion': tecnica.theory[:300] if tecnica.theory else ''
        }

    def _crear_pregunta_completar(self, tecnica):
        texto = tecnica.theory or tecnica.exercise_text or ""
        if not texto:
            return None
        palabras = re.findall(r'\b\w{6,}\b', texto)
        if len(palabras) < 3:
            return None
        palabra_oculta = random.choice(palabras)
        texto_modificado = texto.replace(palabra_oculta, "_______", 1)
        pregunta_texto = f"Completa la siguiente oración:\n\n\"{texto_modificado}\""
        return {
            'pregunta': pregunta_texto,
            'texto_base': texto_modificado,
            'opciones': [],
            'respuesta': palabra_oculta,
            'tipo': 'completar',
            'explicacion': tecnica.theory[:300] if tecnica.theory else ''
        }

    def _crear_pregunta_emparejar(self, tecnica, todas):
        otras = [t for t in todas if t.id != tecnica.id]
        random.shuffle(otras)
        seleccionadas = [tecnica] + otras[:3]
        if len(seleccionadas) < 2:
            return None
        pares = []
        for t in seleccionadas:
            concepto = t.title[:50]
            definicion = t.theory[:80] if t.theory else f"Definición de {concepto}"
            pares.append({'concepto': concepto, 'definicion': definicion})
        definiciones = [p['definicion'] for p in pares]
        random.shuffle(definiciones)
        pregunta_texto = "Empareja cada concepto con su definición:\n\n"
        for i, p in enumerate(pares):
            pregunta_texto += f"{i+1}. {p['concepto']}\n"
        pregunta_texto += "\nDefiniciones:\n"
        for i, d in enumerate(definiciones):
            pregunta_texto += f"{chr(65+i)}. {d}\n"
        respuesta = ", ".join([f"{i+1}-{chr(65+definiciones.index(p['definicion']))}" for i, p in enumerate(pares)])
        return {
            'pregunta': pregunta_texto,
            'texto_base': pregunta_texto,
            'opciones': [],
            'respuesta': respuesta,
            'tipo': 'emparejar',
            'explicacion': tecnica.theory[:300] if tecnica.theory else ''
        }

    def _generar_opciones(self, tecnica, todas):
        opciones = []
        if tecnica.correct_answer:
            opciones.append(tecnica.correct_answer)
            otras = [t.correct_answer for t in todas if t.correct_answer and t.id != tecnica.id]
            random.shuffle(otras)
            distractores = otras[:3]
            while len(distractores) < 3:
                distractores.append("Opción incorrecta")
            opciones.extend(distractores)
            random.shuffle(opciones)
        return opciones
