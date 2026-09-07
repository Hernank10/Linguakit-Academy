import random
import re
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.content.models import LinguisticTechnique, Curso, Leccion, Ejercicio, Evaluacion

class Command(BaseCommand):
    help = 'Genera cursos, lecciones, 100 ejercicios por lección y evaluaciones'

    def add_arguments(self, parser):
        parser.add_argument('--num-cursos', type=int, default=20)
        parser.add_argument('--ejercicios-por-leccion', type=int, default=100)
        parser.add_argument('--preguntas-por-evaluacion', type=int, default=100)
        parser.add_argument('--clear', action='store_true')
        parser.add_argument('--force', action='store_true')

    @transaction.atomic
    def handle(self, *args, **options):
        self.force = options['force']
        num_cursos = min(options['num_cursos'], 50)
        ejercicios_por_leccion = min(options['ejercicios_por_leccion'], 100)
        preguntas_por_evaluacion = options['preguntas_por_evaluacion']
        clear = options['clear']

        if clear:
            self._limpiar_datos()

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

        seleccionadas = sorted(agrupadas.items(), key=lambda x: len(x[1]), reverse=True)[:num_cursos]

        for categoria, tecnicas_cat in seleccionadas:
            curso = self._crear_curso(categoria, tecnicas_cat)
            self.stdout.write(f'✅ Curso: {curso.titulo}')

            lecciones = self._crear_lecciones(curso, tecnicas_cat)
            self.stdout.write(f'   📖 {len(lecciones)} lecciones')

            for idx, leccion in enumerate(lecciones):
                nivel = min(idx + 1, 5)
                ejercicios = self._crear_ejercicios(leccion, ejercicios_por_leccion, tecnicas_cat, nivel)
                self.stdout.write(f'      📝 Lección {idx+1}: {len(ejercicios)} ejercicios (dificultad {nivel})')

            evaluacion = self._crear_evaluacion(curso, tecnicas_cat, preguntas_por_evaluacion)
            if evaluacion:
                self.stdout.write(f'   📊 Evaluación: {len(evaluacion.preguntas)} preguntas')

        self.stdout.write(self.style.SUCCESS('\n🎉 Generación completada'))

    def _limpiar_datos(self):
        Evaluacion.objects.all().delete()
        Ejercicio.objects.all().delete()
        Leccion.objects.all().delete()
        Curso.objects.all().delete()

    def _crear_curso(self, categoria, tecnicas):
        titulo = f"Curso de {categoria.capitalize()}"
        descripcion = f"Curso completo sobre {categoria}. {len(tecnicas)} técnicas."
        curso, _ = Curso.objects.get_or_create(
            titulo=titulo,
            defaults={'descripcion': descripcion, 'categoria': categoria}
        )
        return curso

    def _crear_lecciones(self, curso, tecnicas):
        if curso.lecciones.exists() and not self.force:
            return list(curso.lecciones.all().order_by('orden'))
        if self.force:
            curso.lecciones.all().delete()

        random.shuffle(tecnicas)
        lecciones = []
        tamano = 5
        for i in range(0, len(tecnicas), tamano):
            grupo = tecnicas[i:i+tamano]
            if not grupo:
                continue
            titulo = f"Lección {i//tamano + 1}: {grupo[0].title[:50]}"
            descripcion = " | ".join([t.theory[:100] for t in grupo if t.theory])[:500]
            leccion, _ = Leccion.objects.get_or_create(
                curso=curso,
                titulo=titulo,
                defaults={'descripcion': descripcion, 'orden': i//tamano + 1}
            )
            lecciones.append(leccion)
        return lecciones

    def _crear_ejercicios(self, leccion, cantidad, tecnicas_cat, nivel_dificultad):
        if leccion.ejercicios.exists() and not self.force:
            return list(leccion.ejercicios.all())
        if self.force:
            leccion.ejercicios.all().delete()

        tecnicas_disponibles = list(tecnicas_cat)
        if len(tecnicas_disponibles) < cantidad:
            tecnicas_disponibles = tecnicas_disponibles * (cantidad // len(tecnicas_disponibles) + 1)
        random.shuffle(tecnicas_disponibles)

        seleccionadas = tecnicas_disponibles[:cantidad]
        ejercicios = []
        tipos = ['multiple', 'vf', 'completar', 'emparejar']

        for i, t in enumerate(seleccionadas):
            tipo = tipos[i % len(tipos)]
            dif = max(1, min(nivel_dificultad + random.randint(-1, 1), 5))

            if tipo == 'multiple':
                ejercicio = self._crear_multiple(t, tecnicas_cat, dif, leccion)
            elif tipo == 'vf':
                ejercicio = self._crear_vf(t, dif, leccion)
            elif tipo == 'completar':
                ejercicio = self._crear_completar(t, dif, leccion)
            else:
                ejercicio = self._crear_emparejar(t, tecnicas_cat, dif, leccion)

            if ejercicio:
                ejercicios.append(ejercicio)

        return ejercicios

    def _crear_multiple(self, tecnica, todas, dificultad, leccion):
        pregunta = tecnica.exercise_text or tecnica.theory[:200] or "¿Cuál es el concepto principal?"
        respuesta = tecnica.correct_answer or "Revisa la teoría"
        opciones = self._generar_opciones(tecnica, todas, dificultad)
        explicacion = tecnica.theory[:300] if tecnica.theory else "Revisa la técnica."

        ejercicio, _ = Ejercicio.objects.get_or_create(
            leccion=leccion,
            titulo=f"🎯 {tecnica.title[:40]}",
            defaults={
                'pregunta': pregunta,
                'opciones': opciones,
                'respuesta_correcta': respuesta,
                'explicacion': explicacion,
                'puntos': 10 + dificultad * 2
            }
        )
        return ejercicio

    def _crear_vf(self, tecnica, dificultad, leccion):
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
        pregunta = f"¿Es correcta la siguiente afirmación?\n\n\"{frase}\""
        opciones = ["Verdadero", "Falso"]
        respuesta = "Verdadero" if es_verdadero else "Falso"
        ejercicio, _ = Ejercicio.objects.get_or_create(
            leccion=leccion,
            titulo=f"⚖️ {tecnica.title[:40]}",
            defaults={
                'pregunta': pregunta,
                'opciones': opciones,
                'respuesta_correcta': respuesta,
                'explicacion': f"📖 Explicación: {tecnica.theory[:300] if tecnica.theory else 'Revisa la técnica.'}",
                'puntos': 5 + dificultad
            }
        )
        return ejercicio

    def _crear_completar(self, tecnica, dificultad, leccion):
        texto = tecnica.theory or tecnica.exercise_text or ""
        if not texto:
            return None
        palabras = re.findall(r'\b\w{6,}\b', texto)
        if len(palabras) < 3:
            return None
        palabra_oculta = random.choice(palabras)
        respuesta = palabra_oculta
        texto_modificado = texto.replace(palabra_oculta, "_______", 1)
        pregunta = f"Completa la siguiente oración:\n\n\"{texto_modificado}\""
        ejercicio, _ = Ejercicio.objects.get_or_create(
            leccion=leccion,
            titulo=f"✏️ {tecnica.title[:40]}",
            defaults={
                'pregunta': pregunta,
                'opciones': [],
                'respuesta_correcta': respuesta,
                'explicacion': f"📖 Explicación: {tecnica.theory[:300] if tecnica.theory else 'Revisa la técnica.'}",
                'puntos': 8 + dificultad
            }
        )
        return ejercicio

    def _crear_emparejar(self, tecnica, todas, dificultad, leccion):
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
        pregunta = "Empareja cada concepto con su definición:\n\n"
        for i, p in enumerate(pares):
            pregunta += f"{i+1}. {p['concepto']}\n"
        pregunta += "\nDefiniciones:\n"
        for i, d in enumerate(definiciones):
            pregunta += f"{chr(65+i)}. {d}\n"
        respuesta = ", ".join([f"{i+1}-{chr(65+definiciones.index(p['definicion']))}" for i, p in enumerate(pares)])
        ejercicio, _ = Ejercicio.objects.get_or_create(
            leccion=leccion,
            titulo=f"🔗 {tecnica.title[:40]}",
            defaults={
                'pregunta': pregunta,
                'opciones': [],
                'respuesta_correcta': respuesta,
                'explicacion': f"📖 Explicación: {tecnica.theory[:300] if tecnica.theory else 'Revisa las técnicas.'}",
                'puntos': 15 + dificultad * 2
            }
        )
        return ejercicio

    def _generar_opciones(self, tecnica, todas, dificultad):
        opciones = []
        if tecnica.correct_answer:
            opciones.append(tecnica.correct_answer)
            num_distractores = min(dificultad + 1, 3)
            otras = [t.correct_answer for t in todas if t.correct_answer and t.id != tecnica.id]
            random.shuffle(otras)
            distractores = otras[:num_distractores]
            while len(distractores) < num_distractores:
                distractores.append(f"Opción incorrecta {len(distractores)+1}")
            opciones.extend(distractores)
            random.shuffle(opciones)
        return opciones

    def _crear_evaluacion(self, curso, tecnicas, cantidad):
        evaluacion_existente = Evaluacion.objects.filter(curso=curso).first()
        if evaluacion_existente and not self.force:
            return evaluacion_existente
        if self.force and evaluacion_existente:
            evaluacion_existente.delete()

        if len(tecnicas) < cantidad:
            tecnicas_eval = list(tecnicas) * (cantidad // len(tecnicas) + 1)
        else:
            tecnicas_eval = random.sample(tecnicas, cantidad)

        preguntas = []
        for t in tecnicas_eval[:cantidad]:
            texto = t.theory or t.exercise_text
            if not texto:
                continue
            opciones = self._generar_opciones(t, tecnicas, random.randint(1, 3))
            preguntas.append({
                'pregunta': f"{t.title[:80]}",
                'texto_base': texto[:200],
                'opciones': opciones,
                'respuesta': t.correct_answer or "Revisa la técnica",
                'explicacion': t.theory[:300] if t.theory else ''
            })

        if not preguntas:
            return None

        evaluacion, _ = Evaluacion.objects.get_or_create(
            curso=curso,
            titulo=f"Evaluación de {curso.titulo}",
            defaults={
                'descripcion': f"Evalúa tu conocimiento sobre {curso.categoria}. {len(preguntas)} preguntas.",
                'preguntas': preguntas,
                'puntaje_total': len(preguntas) * 10
            }
        )
        return evaluacion
