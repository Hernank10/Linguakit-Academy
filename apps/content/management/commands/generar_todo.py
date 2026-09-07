import random
import re
import hashlib
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.content.models import LinguisticTechnique, Curso, Leccion, Ejercicio, Evaluacion, ProgresoEstudiante, Certificado

User = get_user_model()

class Command(BaseCommand):
    help = 'Genera TODO el sistema: cursos, lecciones, 100 ejercicios/lección, evaluaciones con 1000 preguntas, usuarios, progreso y certificados'

    def add_arguments(self, parser):
        parser.add_argument('--num-cursos', type=int, default=15, help='Número de cursos a generar')
        parser.add_argument('--num-estudiantes', type=int, default=10, help='Número de estudiantes a crear')
        parser.add_argument('--num-profesores', type=int, default=3, help='Número de profesores a crear')
        parser.add_argument('--ejercicios-por-leccion', type=int, default=100, help='Ejercicios por lección')
        parser.add_argument('--preguntas-por-evaluacion', type=int, default=1000, help='Preguntas por evaluación')
        parser.add_argument('--clear', action='store_true', help='Limpiar todo antes de generar')
        parser.add_argument('--force', action='store_true', help='Forzar recreación de todo')
        parser.add_argument('--password', type=str, default='password123', help='Contraseña para usuarios nuevos')

    @transaction.atomic
    def handle(self, *args, **options):
        self.force = options['force']
        num_cursos = min(options['num_cursos'], 30)
        num_estudiantes = options['num_estudiantes']
        num_profesores = options['num_profesores']
        ejercicios_por_leccion = options['ejercicios_por_leccion']
        preguntas_por_evaluacion = options['preguntas_por_evaluacion']
        clear = options['clear']
        password = options['password']

        if clear:
            self._limpiar_todo()
            self.stdout.write('🗑️ Todo limpiado')

        # 1. Obtener técnicas
        tecnicas = list(LinguisticTechnique.objects.all())
        if not tecnicas:
            self.stdout.write(self.style.ERROR('❌ No hay técnicas. Importa primero los datos.'))
            return

        self.stdout.write(f'📚 {len(tecnicas)} técnicas disponibles')

        # 2. Generar cursos
        cursos_creados = self._generar_cursos(tecnicas, num_cursos)
        self.stdout.write(f'✅ Cursos generados: {len(cursos_creados)}')

        # 3. Generar lecciones, ejercicios y evaluaciones
        for curso in cursos_creados:
            lecciones = self._generar_lecciones(curso, tecnicas)
            self.stdout.write(f'   📖 {curso.titulo[:30]}: {len(lecciones)} lecciones')

            for leccion in lecciones:
                ejercicios = self._generar_ejercicios(leccion, tecnicas, ejercicios_por_leccion)
                self.stdout.write(f'      📝 {leccion.titulo[:30]}: {len(ejercicios)} ejercicios')

            evaluacion = self._generar_evaluacion(curso, tecnicas, preguntas_por_evaluacion)
            if evaluacion:
                self.stdout.write(f'   📊 Evaluación: {len(evaluacion.preguntas)} preguntas')

        # 4. Crear usuarios
        usuarios = self._crear_usuarios(num_estudiantes, num_profesores, password)
        self.stdout.write(f'👥 Usuarios creados: {len(usuarios)}')

        # 5. Generar progreso simulado
        progresos = self._generar_progreso_simulado(usuarios, cursos_creados)
        self.stdout.write(f'📈 Progresos generados: {len(progresos)}')

        # 6. Generar certificados
        certificados = self._generar_certificados()
        self.stdout.write(f'📜 Certificados generados: {certificados}')

        # 7. Resumen final
        self._mostrar_resumen()

        self.stdout.write(self.style.SUCCESS('\n🎉 TODO GENERADO EXITOSAMENTE'))

    # ==================== LIMPIEZA ====================

    def _limpiar_todo(self):
        Certificado.objects.all().delete()
        ProgresoEstudiante.objects.all().delete()
        Ejercicio.objects.all().delete()
        Leccion.objects.all().delete()
        Evaluacion.objects.all().delete()
        Curso.objects.all().delete()

    # ==================== CURSOS ====================

    def _generar_cursos(self, tecnicas, num_cursos):
        # Agrupar por categoría y nivel
        agrupadas = {}
        for t in tecnicas:
            cat = t.category or 'Sin categoría'
            nivel = t.level or 'B1'
            agrupadas.setdefault((cat, nivel), []).append(t)

        seleccionadas = sorted(agrupadas.items(), key=lambda x: len(x[1]), reverse=True)[:num_cursos]

        cursos = []
        for (categoria, nivel), tecnicas_cat in seleccionadas:
            titulo = f"Curso de {categoria.capitalize()} (Nivel {nivel})"
            descripcion = f"Curso completo sobre {categoria}. {len(tecnicas_cat)} técnicas. Incluye 100 ejercicios por lección y certificación."
            curso, creado = Curso.objects.get_or_create(
                titulo=titulo,
                defaults={'descripcion': descripcion, 'categoria': categoria, 'nivel': nivel}
            )
            cursos.append(curso)
        return cursos

    # ==================== LECCIONES ====================

    def _generar_lecciones(self, curso, tecnicas):
        if curso.lecciones.exists() and not self.force:
            return list(curso.lecciones.all().order_by('orden'))

        if self.force:
            curso.lecciones.all().delete()

        tecnicas_cat = [t for t in tecnicas if t.category == curso.categoria]
        if not tecnicas_cat:
            tecnicas_cat = tecnicas

        random.shuffle(tecnicas_cat)
        lecciones = []
        tamano = 5
        for i in range(0, len(tecnicas_cat), tamano):
            grupo = tecnicas_cat[i:i+tamano]
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

    # ==================== EJERCICIOS ====================

    def _generar_ejercicios(self, leccion, tecnicas, cantidad):
        if leccion.ejercicios.exists() and not self.force:
            return list(leccion.ejercicios.all())

        if self.force:
            leccion.ejercicios.all().delete()

        tecnicas_cat = [t for t in tecnicas if t.category == leccion.curso.categoria]
        if not tecnicas_cat:
            tecnicas_cat = tecnicas

        if len(tecnicas_cat) < cantidad:
            tecnicas_cat = tecnicas_cat * (cantidad // len(tecnicas_cat) + 1)

        random.shuffle(tecnicas_cat)
        seleccionadas = tecnicas_cat[:cantidad]
        ejercicios = []
        tipos = ['multiple', 'vf', 'completar', 'emparejar']

        for i, t in enumerate(seleccionadas):
            tipo = tipos[i % len(tipos)]
            if tipo == 'multiple':
                ejercicio = self._crear_ejercicio_multiple(leccion, t, tecnicas_cat)
            elif tipo == 'vf':
                ejercicio = self._crear_ejercicio_vf(leccion, t)
            elif tipo == 'completar':
                ejercicio = self._crear_ejercicio_completar(leccion, t)
            else:
                ejercicio = self._crear_ejercicio_emparejar(leccion, t, tecnicas_cat)

            if ejercicio:
                ejercicios.append(ejercicio)

        return ejercicios

    def _crear_ejercicio_multiple(self, leccion, tecnica, todas):
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

    def _crear_ejercicio_vf(self, leccion, tecnica):
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

    def _crear_ejercicio_completar(self, leccion, tecnica):
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

    def _crear_ejercicio_emparejar(self, leccion, tecnica, todas):
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

    # ==================== EVALUACIONES ====================

    def _generar_evaluacion(self, curso, tecnicas, cantidad):
        evaluacion_existente = Evaluacion.objects.filter(curso=curso).first()
        if evaluacion_existente and not self.force:
            return evaluacion_existente

        if self.force and evaluacion_existente:
            evaluacion_existente.delete()

        tecnicas_cat = [t for t in tecnicas if t.category == curso.categoria]
        if len(tecnicas_cat) < cantidad:
            otras = [t for t in tecnicas if t.category != curso.categoria]
            random.shuffle(otras)
            faltantes = cantidad - len(tecnicas_cat)
            tecnicas_cat.extend(otras[:faltantes])

        if len(tecnicas_cat) < cantidad:
            tecnicas_cat = tecnicas_cat * (cantidad // len(tecnicas_cat) + 1)

        random.shuffle(tecnicas_cat)
        seleccionadas = tecnicas_cat[:cantidad]

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
            return None

        evaluacion = Evaluacion.objects.create(
            curso=curso,
            titulo=f"Evaluación Masiva de {curso.titulo}",
            descripcion=f"Evaluación con {len(preguntas)} preguntas sobre {curso.categoria}",
            preguntas=preguntas,
            puntaje_total=len(preguntas) * 10
        )
        return evaluacion

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

    # ==================== USUARIOS ====================

    def _crear_usuarios(self, num_estudiantes, num_profesores, password):
        # Admin
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser('admin', 'admin@linguakit.com', password)

        # Profesores
        profesores = []
        for i in range(1, num_profesores + 1):
            username = f'profesor{i}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username, f'{username}@linguakit.com', password)
                user.is_staff = True
                user.save()
                profesores.append(user)

        # Estudiantes
        estudiantes = []
        for i in range(1, num_estudiantes + 1):
            username = f'estudiante{i}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username, f'{username}@linguakit.com', password)
                estudiantes.append(user)

        return estudiantes + profesores

    # ==================== PROGRESO SIMULADO ====================

    def _generar_progreso_simulado(self, usuarios, cursos):
        progresos = []
        estudiantes = [u for u in usuarios if not u.is_staff and not u.is_superuser]

        if not estudiantes or not cursos:
            return progresos

        for estudiante in estudiantes:
            # Cada estudiante se inscribe en 2-4 cursos aleatorios
            num_cursos = random.randint(2, min(4, len(cursos)))
            cursos_seleccionados = random.sample(cursos, num_cursos)

            for curso in cursos_seleccionados:
                # Simular progreso
                completado = random.choice([True, False])
                porcentaje = random.uniform(40, 100) if completado else random.uniform(10, 80)
                ejercicios_totales = sum(l.ejercicios.count() for l in curso.lecciones.all())
                ejercicios_completados = int(ejercicios_totales * (porcentaje / 100))
                ejercicios_correctos = int(ejercicios_completados * random.uniform(0.6, 0.95))
                puntaje = ejercicios_correctos * random.randint(5, 15)

                progreso, _ = ProgresoEstudiante.objects.get_or_create(
                    estudiante=estudiante,
                    curso=curso,
                    defaults={
                        'lecciones_completadas': random.randint(0, curso.lecciones.count()),
                        'ejercicios_completados': ejercicios_completados,
                        'ejercicios_correctos': ejercicios_correctos,
                        'puntaje_total': puntaje,
                        'porcentaje_completado': porcentaje,
                        'completado': completado,
                        'fecha_completado': timezone.now() - timedelta(days=random.randint(0, 10)) if completado else None
                    }
                )
                progresos.append(progreso)

        return progresos

    # ==================== CERTIFICADOS ====================

    def _generar_certificados(self):
        progresos = ProgresoEstudiante.objects.filter(
            completado=True,
            porcentaje_completado__gte=80.0
        )

        certificados_creados = 0
        for progreso in progresos:
            if Certificado.objects.filter(estudiante=progreso.estudiante, curso=progreso.curso).exists():
                continue

            codigo = hashlib.md5(
                f"{progreso.estudiante.id}{progreso.curso.id}{datetime.now().isoformat()}".encode()
            ).hexdigest()[:12].upper()

            certificado = Certificado.objects.create(
                estudiante=progreso.estudiante,
                curso=progreso.curso,
                codigo=codigo,
                puntaje_final=progreso.puntaje_total / max(progreso.ejercicios_completados, 1) * 100
            )
            certificados_creados += 1

        return certificados_creados

    # ==================== RESUMEN ====================

    def _mostrar_resumen(self):
        self.stdout.write('\n' + '='*50)
        self.stdout.write('📊 RESUMEN FINAL')
        self.stdout.write('='*50)
        self.stdout.write(f'📚 Técnicas: {LinguisticTechnique.objects.count()}')
        self.stdout.write(f'📂 Cursos: {Curso.objects.count()}')
        self.stdout.write(f'📖 Lecciones: {Leccion.objects.count()}')
        self.stdout.write(f'📝 Ejercicios: {Ejercicio.objects.count()}')
        self.stdout.write(f'📊 Evaluaciones: {Evaluacion.objects.count()}')
        total_preguntas = sum(len(e.preguntas) for e in Evaluacion.objects.all())
        self.stdout.write(f'❓ Preguntas en evaluaciones: {total_preguntas}')
        self.stdout.write(f'👥 Usuarios: {User.objects.count()}')
        self.stdout.write(f'📈 Progresos: {ProgresoEstudiante.objects.count()}')
        self.stdout.write(f'📜 Certificados: {Certificado.objects.count()}')
        self.stdout.write('='*50)
