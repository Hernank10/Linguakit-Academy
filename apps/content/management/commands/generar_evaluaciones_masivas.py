import random
import re
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.content.models import LinguisticTechnique, Curso, Evaluacion

class Command(BaseCommand):
    help = 'Genera evaluaciones con 1000 preguntas para cada curso'

    def add_arguments(self, parser):
        parser.add_argument('--num-preguntas', type=int, default=1000, help='Número de preguntas por evaluación')
        parser.add_argument('--force', action='store_true', help='Reemplazar evaluaciones existentes')

    @transaction.atomic
    def handle(self, *args, **options):
        num_preguntas = options['num_preguntas']
        force = options['force']

        # Obtener todas las técnicas
        tecnicas = list(LinguisticTechnique.objects.all())
        if not tecnicas:
            self.stdout.write(self.style.ERROR('❌ No hay técnicas'))
            return

        self.stdout.write(f'📚 {len(tecnicas)} técnicas disponibles')

        # Obtener todos los cursos
        cursos = Curso.objects.all()
        if not cursos:
            self.stdout.write(self.style.ERROR('❌ No hay cursos. Genera primero cursos.'))
            return

        self.stdout.write(f'📂 {len(cursos)} cursos encontrados')

        total_preguntas = 0
        for curso in cursos:
            # Verificar si ya tiene evaluación
            evaluacion_existente = Evaluacion.objects.filter(curso=curso).first()
            if evaluacion_existente and not force:
                self.stdout.write(f'ℹ️ Curso "{curso.titulo[:30]}" ya tiene evaluación. Usa --force para reemplazar.')
                continue

            if force and evaluacion_existente:
                evaluacion_existente.delete()
                self.stdout.write(f'🔄 Reemplazando evaluación de "{curso.titulo[:30]}"')

            # Obtener técnicas de la categoría del curso
            tecnicas_cat = [t for t in tecnicas if t.category == curso.categoria]
            if len(tecnicas_cat) < num_preguntas:
                # Si no hay suficientes, combinar con otras técnicas
                otras = [t for t in tecnicas if t.category != curso.categoria]
                random.shuffle(otras)
                faltantes = num_preguntas - len(tecnicas_cat)
                tecnicas_cat.extend(otras[:faltantes])

            # Si aún no hay suficientes, repetir
            if len(tecnicas_cat) < num_preguntas:
                tecnicas_cat = tecnicas_cat * (num_preguntas // len(tecnicas_cat) + 1)

            random.shuffle(tecnicas_cat)
            seleccionadas = tecnicas_cat[:num_preguntas]

            # Generar preguntas
            preguntas = []
            tipos = ['multiple', 'vf', 'completar', 'emparejar']

            for i, t in enumerate(seleccionadas):
                tipo = tipos[i % len(tipos)]
                if tipo == 'multiple':
                    pregunta = self._crear_pregunta_multiple(t, tecnicas)
                elif tipo == 'vf':
                    pregunta = self._crear_pregunta_vf(t)
                elif tipo == 'completar':
                    pregunta = self._crear_pregunta_completar(t)
                else:
                    pregunta = self._crear_pregunta_emparejar(t, tecnicas)

                if pregunta:
                    preguntas.append(pregunta)

            if not preguntas:
                self.stdout.write(self.style.ERROR(f'❌ No se pudieron generar preguntas para "{curso.titulo}"'))
                continue

            # Crear evaluación
            evaluacion = Evaluacion.objects.create(
                curso=curso,
                titulo=f"Evaluación Masiva de {curso.titulo}",
                descripcion=f"Evaluación con {len(preguntas)} preguntas sobre {curso.categoria}. ¡Demuestra lo que has aprendido!",
                preguntas=preguntas,
                puntaje_total=len(preguntas) * 10
            )

            total_preguntas += len(preguntas)
            self.stdout.write(f'✅ Curso "{curso.titulo[:30]}": {len(preguntas)} preguntas generadas')

        self.stdout.write(self.style.SUCCESS(f'\n🎉 Total: {total_preguntas} preguntas generadas en {cursos.count()} evaluaciones'))

    # ==================== FUNCIONES GENERADORAS DE PREGUNTAS ====================

    def _crear_pregunta_multiple(self, tecnica, todas):
        pregunta = tecnica.exercise_text or tecnica.theory[:200] or "¿Cuál es el concepto principal?"
        respuesta = tecnica.correct_answer or "Revisa la teoría"
        opciones = self._generar_opciones(tecnica, todas)
        return {
            'pregunta': f"[Múltiple] {pregunta}",
            'texto_base': tecnica.theory[:200] if tecnica.theory else '',
            'opciones': opciones,
            'respuesta': respuesta,
            'tipo': 'multiple',
            'dificultad': random.randint(1, 5),
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
        return {
            'pregunta': f"[V/F] ¿Es correcta? \"{frase}\"",
            'texto_base': frase,
            'opciones': ["Verdadero", "Falso"],
            'respuesta': "Verdadero" if es_verdadero else "Falso",
            'tipo': 'vf',
            'dificultad': random.randint(1, 3),
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
        return {
            'pregunta': f"[Completar] {texto_modificado}",
            'texto_base': texto,
            'opciones': [],
            'respuesta': palabra_oculta,
            'tipo': 'completar',
            'dificultad': random.randint(2, 4),
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
        pregunta = "Empareja cada concepto con su definición:\n"
        for i, p in enumerate(pares):
            pregunta += f"{i+1}. {p['concepto']}\n"
        pregunta += "\nDefiniciones:\n"
        for i, d in enumerate(definiciones):
            pregunta += f"{chr(65+i)}. {d}\n"
        respuesta = ", ".join([f"{i+1}-{chr(65+definiciones.index(p['definicion']))}" for i, p in enumerate(pares)])
        return {
            'pregunta': f"[Emparejar] {pregunta}",
            'texto_base': '',
            'opciones': [],
            'respuesta': respuesta,
            'tipo': 'emparejar',
            'dificultad': random.randint(3, 5),
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
