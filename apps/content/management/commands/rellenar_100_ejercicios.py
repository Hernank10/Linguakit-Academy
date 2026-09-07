import random
import re
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.content.models import LinguisticTechnique, Leccion, Ejercicio

class Command(BaseCommand):
    help = 'Asegura que cada lección tenga exactamente 100 ejercicios (crea/actualiza)'

    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true', help='Eliminar y regenerar todos los ejercicios de cada lección')
        parser.add_argument('--min-ejercicios', type=int, default=100, help='Número mínimo de ejercicios por lección')

    @transaction.atomic
    def handle(self, *args, **options):
        force = options['force']
        min_ejercicios = options['min_ejercicios']

        # Obtener todas las técnicas
        tecnicas = list(LinguisticTechnique.objects.all())
        if not tecnicas:
            self.stdout.write(self.style.ERROR('❌ No hay técnicas'))
            return

        # Obtener todas las lecciones
        lecciones = Leccion.objects.all()
        if not lecciones:
            self.stdout.write(self.style.ERROR('❌ No hay lecciones'))
            return

        self.stdout.write(f'📚 {len(tecnicas)} técnicas disponibles')
        self.stdout.write(f'📖 {len(lecciones)} lecciones encontradas')

        total_creados = 0
        total_actualizados = 0

        for leccion in lecciones:
            # Contar ejercicios actuales
            ejercicios_actuales = list(leccion.ejercicios.all())
            cantidad_actual = len(ejercicios_actuales)

            if force or cantidad_actual < min_ejercicios:
                if force:
                    # Eliminar todos y regenerar
                    leccion.ejercicios.all().delete()
                    cantidad_actual = 0
                    self.stdout.write(f'🔄 Regenerando lección: {leccion.titulo[:40]}...')

                # Obtener técnicas de la categoría del curso
                categoria = leccion.curso.categoria
                tecnicas_cat = [t for t in tecnicas if t.category == categoria]
                if not tecnicas_cat:
                    tecnicas_cat = tecnicas  # fallback

                # Generar hasta min_ejercicios
                necesarios = min_ejercicios - cantidad_actual
                if necesarios <= 0:
                    continue

                # Asegurar suficientes técnicas
                if len(tecnicas_cat) < necesarios:
                    tecnicas_cat = tecnicas_cat * (necesarios // len(tecnicas_cat) + 1)
                random.shuffle(tecnicas_cat)

                seleccionadas = tecnicas_cat[:necesarios]
                tipos = ['multiple', 'vf', 'completar', 'emparejar']

                for i, t in enumerate(seleccionadas):
                    tipo = tipos[i % len(tipos)]
                    if tipo == 'multiple':
                        ejercicio = self._crear_multiple(leccion, t, tecnicas_cat)
                    elif tipo == 'vf':
                        ejercicio = self._crear_vf(leccion, t)
                    elif tipo == 'completar':
                        ejercicio = self._crear_completar(leccion, t)
                    else:
                        ejercicio = self._crear_emparejar(leccion, t, tecnicas_cat)

                    if ejercicio:
                        total_creados += 1

                self.stdout.write(f'✅ {leccion.titulo[:40]}: ahora tiene {leccion.ejercicios.count()} ejercicios')

        self.stdout.write(self.style.SUCCESS(f'\n🎉 Total ejercicios creados/actualizados: {total_creados}'))
        self.stdout.write(f'📊 Total ejercicios en BD: {Ejercicio.objects.count()}')

    # ==================== FUNCIONES GENERADORAS ====================

    def _crear_multiple(self, leccion, tecnica, todas):
        pregunta = tecnica.exercise_text or tecnica.theory[:200] or "¿Cuál es el concepto principal?"
        respuesta = tecnica.correct_answer or "Revisa la teoría"
        opciones = self._generar_opciones(tecnica, todas)
        explicacion = tecnica.theory[:300] if tecnica.theory else "Revisa la técnica."
        ejemplo = tecnica.example[:200] if tecnica.example else ""
        texto_explicacion = f"📖 Explicación: {explicacion}\n💡 Ejemplo: {ejemplo}" if ejemplo else explicacion

        ejercicio = Ejercicio.objects.create(
            leccion=leccion,
            titulo=f"🎯 {tecnica.title[:40]}",
            pregunta=pregunta,
            opciones=opciones,
            respuesta_correcta=respuesta,
            explicacion=texto_explicacion,
            puntos=10 + random.randint(0, 10)
        )
        return ejercicio

    def _crear_vf(self, leccion, tecnica):
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
        ejercicio = Ejercicio.objects.create(
            leccion=leccion,
            titulo=f"⚖️ {tecnica.title[:40]}",
            pregunta=pregunta,
            opciones=opciones,
            respuesta_correcta=respuesta,
            explicacion=f"📖 Explicación: {tecnica.theory[:300] if tecnica.theory else 'Revisa la técnica.'}",
            puntos=5 + random.randint(0, 5)
        )
        return ejercicio

    def _crear_completar(self, leccion, tecnica):
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
        ejercicio = Ejercicio.objects.create(
            leccion=leccion,
            titulo=f"✏️ {tecnica.title[:40]}",
            pregunta=pregunta,
            opciones=[],
            respuesta_correcta=respuesta,
            explicacion=f"📖 Explicación: {tecnica.theory[:300] if tecnica.theory else 'Revisa la técnica.'}",
            puntos=8 + random.randint(0, 5)
        )
        return ejercicio

    def _crear_emparejar(self, leccion, tecnica, todas):
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
        ejercicio = Ejercicio.objects.create(
            leccion=leccion,
            titulo=f"🔗 {tecnica.title[:40]}",
            pregunta=pregunta,
            opciones=[],
            respuesta_correcta=respuesta,
            explicacion=f"📖 Explicación: {tecnica.theory[:300] if tecnica.theory else 'Revisa las técnicas.'}",
            puntos=15 + random.randint(0, 10)
        )
        return ejercicio

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
