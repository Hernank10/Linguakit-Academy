#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de ejercicios interactivos a partir de los datos de retórica y etimologías.
Crea un HTML con estilo Bootstrap, preguntas aleatorias y autoevaluación.
"""

import json
import random
import html
import os
from typing import List, Dict, Any

# ------------------------------------------------------------
# 1. Datos de ejemplo (puedes cargarlos desde archivos JSON)
# ------------------------------------------------------------
RETORICA_DATA = [
    {
        "id": 1,
        "name": "Anáfora",
        "teoria": "Repetición de una o varias palabras al comienzo de frases o versos.",
        "ejemplo": "¡Aquí fue Troya! ¡Aquí mi espada! ¡Aquí mi valor!"
    },
    {
        "id": 2,
        "name": "Metáfora",
        "teoria": "Identificación de un término real con otro imaginario.",
        "ejemplo": "Tus ojos son dos luceros."
    },
    {
        "id": 3,
        "name": "Ironía",
        "teoria": "Expresar lo contrario de lo que se piensa.",
        "ejemplo": "¡Qué día tan hermoso! (durante un diluvio)"
    },
    {
        "id": 4,
        "name": "Hipérbole",
        "teoria": "Exageración intencionada.",
        "ejemplo": "Te lo he dicho un millón de veces."
    },
    {
        "id": 5,
        "name": "Oxímoron",
        "teoria": "Unión de términos opuestos.",
        "ejemplo": "Silencio atronador."
    },
    {
        "id": 6,
        "name": "Polisíndeton",
        "teoria": "Uso abundante de conjunciones.",
        "ejemplo": "Y corre y vuela y grita."
    },
    {
        "id": 7,
        "name": "Asíndeton",
        "teoria": "Omisión de conjunciones.",
        "ejemplo": "Llegué, vi, vencí."
    },
    {
        "id": 8,
        "name": "Quiasmo",
        "teoria": "Estructura cruzada AB/BA.",
        "ejemplo": "Cuando quiero llorar no lloro, y a veces lloro sin querer."
    }
]

ETIMOLOGIA_DATA = [
    {
        "id": 1,
        "element": "bio",
        "origin": "griego",
        "meaning": "vida",
        "examples": "biología, biografía",
        "originalScript": "βίος"
    },
    {
        "id": 2,
        "element": "geo",
        "origin": "griego",
        "meaning": "tierra",
        "examples": "geografía, geología",
        "originalScript": "γῆ"
    },
    {
        "id": 3,
        "element": "aqua",
        "origin": "latín",
        "meaning": "agua",
        "examples": "acuático, acueducto",
        "originalScript": "aqua"
    },
    {
        "id": 4,
        "element": "chron",
        "origin": "griego",
        "meaning": "tiempo",
        "examples": "cronología, crónico",
        "originalScript": "χρόνος"
    },
    {
        "id": 5,
        "element": "phone",
        "origin": "griego",
        "meaning": "sonido",
        "examples": "teléfono, fonética",
        "originalScript": "φωνή"
    }
]

# ------------------------------------------------------------
# 2. Funciones para generar preguntas
# ------------------------------------------------------------
def generar_pregunta_definicion(item: Dict[str, Any], tema: str) -> Dict[str, Any]:
    """Genera una pregunta de definición (¿Qué es X?) con opciones múltiples."""
    if tema == "retorica":
        termino = item["name"]
        respuesta_correcta = item["teoria"]
        distractores = [
            "Figura que consiste en repetir sonidos",
            "Exageración desmesurada",
            "Orden inverso de palabras"
        ]
        # Intentar distractores más relevantes
        if "Anáfora" in termino:
            distractores = ["Repetición al final", "Omisión de conjunciones", "Palabras opuestas"]
        elif "Metáfora" in termino:
            distractores = ["Comparación explícita", "Atribución de cualidades humanas", "Exageración"]
    else:  # etimologia
        termino = item["element"]
        respuesta_correcta = item["meaning"]
        distractores = ["cielo", "fuego", "aire", "escritura"]
    
    opciones = [respuesta_correcta] + random.sample(distractores, min(3, len(distractores)))
    random.shuffle(opciones)
    return {
        "tipo": "definicion",
        "pregunta": f"¿Qué significa '{termino}'?" if tema == "etimologia" else f"¿Qué es la {termino}?",
        "respuesta_correcta": respuesta_correcta,
        "opciones": opciones
    }

def generar_pregunta_aplicacion(item: Dict[str, Any], tema: str) -> Dict[str, Any]:
    """Pregunta de aplicar el concepto: elegir el ejemplo correcto."""
    if tema == "retorica":
        nombre = item["name"]
        ejemplo_correcto = item["ejemplo"]
        # Distractores: ejemplos de otras figuras
        otros_ejemplos = [other["ejemplo"] for other in RETORICA_DATA if other["id"] != item["id"]]
        distractores = random.sample(otros_ejemplos, min(3, len(otros_ejemplos)))
        opciones = [ejemplo_correcto] + distractores
        random.shuffle(opciones)
        return {
            "tipo": "aplicacion",
            "pregunta": f"¿Cuál de los siguientes es un ejemplo de {nombre}?",
            "respuesta_correcta": ejemplo_correcto,
            "opciones": opciones
        }
    else:
        # Para etimología: dar una palabra compuesta y preguntar su significado
        raiz = item["element"]
        significado = item["meaning"]
        palabra_ejemplo = item["examples"].split(",")[0].strip()
        respuesta = f"relacionado con {significado}"
        opciones = [respuesta, "relacionado con el tiempo", "relacionado con el agua", "relacionado con la tierra"]
        random.shuffle(opciones)
        return {
            "tipo": "aplicacion",
            "pregunta": f"La palabra '{palabra_ejemplo}' contiene la raíz '{raiz}'. ¿Qué significado aporta?",
            "respuesta_correcta": respuesta,
            "opciones": opciones
        }

def generar_pregunta_completar(item: Dict[str, Any], tema: str) -> Dict[str, Any]:
    """Pregunta de completar la definición o identificar la figura."""
    if tema == "retorica":
        respuesta = item["name"]
        definicion_corta = item["teoria"].split(".")[0].lower()
        pregunta = f"Completa: La figura retórica que {definicion_corta} se llama..."
        opciones = [respuesta] + [other["name"] for other in random.sample(RETORICA_DATA, min(3, len(RETORICA_DATA)-1))]
        random.shuffle(opciones)
        return {
            "tipo": "completar",
            "pregunta": pregunta,
            "respuesta_correcta": respuesta,
            "opciones": opciones
        }
    else:
        respuesta = item["element"]
        significado = item["meaning"]
        pregunta = f"¿Qué raíz grecolatina significa '{significado}'?"
        opciones = [respuesta] + [other["element"] for other in random.sample(ETIMOLOGIA_DATA, min(3, len(ETIMOLOGIA_DATA)-1))]
        random.shuffle(opciones)
        return {
            "tipo": "completar",
            "pregunta": pregunta,
            "respuesta_correcta": respuesta,
            "opciones": opciones
        }

def generar_examen(tema: str, num_preguntas: int = 10, tipos: List[str] = None) -> List[Dict[str, Any]]:
    """
    Genera un examen con `num_preguntas` preguntas del tema ('retorica' o 'etimologia').
    `tipos` puede ser ['definicion', 'aplicacion', 'completar'] o None para todos.
    """
    if tema == "retorica":
        data = RETORICA_DATA
    else:
        data = ETIMOLOGIA_DATA
    
    if tipos is None:
        tipos = ['definicion', 'aplicacion', 'completar']
    
    preguntas = []
    for _ in range(num_preguntas):
        item = random.choice(data)
        tipo = random.choice(tipos)
        if tipo == 'definicion':
            preguntas.append(generar_pregunta_definicion(item, tema))
        elif tipo == 'aplicacion':
            preguntas.append(generar_pregunta_aplicacion(item, tema))
        else:
            preguntas.append(generar_pregunta_completar(item, tema))
    return preguntas

# ------------------------------------------------------------
# 3. Generador de HTML interactivo
# ------------------------------------------------------------
def generar_html_examen(tema: str, num_preguntas: int = 10) -> str:
    """
    Crea una página HTML con las preguntas, usando Bootstrap y JavaScript para autoevaluación.
    """
    preguntas = generar_examen(tema, num_preguntas)
    
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Examen interactivo de {tema.capitalize()}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        body {{ background: #f8f9fa; }}
        .container {{ max-width: 800px; margin-top: 2rem; }}
        .question-card {{
            background: white;
            border-radius: 1rem;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        }}
        .btn-check-ans {{
            background: #2c3e50;
            color: white;
            border-radius: 2rem;
        }}
        .feedback {{
            margin-top: 1rem;
            padding: 0.75rem;
            border-radius: 0.8rem;
            display: none;
        }}
        .correct {{ background: #d4edda; color: #155724; }}
        .incorrect {{ background: #f8d7da; color: #721c24; }}
    </style>
</head>
<body>
<div class="container">
    <h1 class="text-center mb-4"><i class="fas fa-pen-alt"></i> Ejercicios de {tema.capitalize()}</h1>
    <p class="text-center text-muted">Selecciona la opción correcta y luego haz clic en "Comprobar respuesta".</p>
    <form id="examForm">
"""

    # Generar preguntas en HTML
    for idx, q in enumerate(preguntas):
        html_content += f"""
        <div class="question-card" id="q{idx}">
            <h5><span class="badge bg-secondary me-2">Pregunta {idx+1}</span> {html.escape(q['pregunta'])}</h5>
            <div class="mt-3">
        """
        for opt_idx, opt in enumerate(q['opciones']):
            html_content += f"""
                <div class="form-check">
                    <input class="form-check-input" type="radio" name="q{idx}" id="q{idx}_opt{opt_idx}" value="{html.escape(opt)}">
                    <label class="form-check-label" for="q{idx}_opt{opt_idx}">
                        {html.escape(opt)}
                    </label>
                </div>
            """
        html_content += f"""
            </div>
            <button type="button" class="btn btn-check-ans btn-sm mt-3" data-qidx="{idx}" data-correct="{html.escape(q['respuesta_correcta'])}">
                <i class="fas fa-check-circle"></i> Comprobar respuesta
            </button>
            <div class="feedback" id="fb{idx}"></div>
        </div>
        """
    
    html_content += """
        <div class="d-flex justify-content-between mb-5">
            <button type="button" id="checkAllBtn" class="btn btn-primary">Revisar todas</button>
            <button type="button" id="resetBtn" class="btn btn-secondary">Limpiar respuestas</button>
        </div>
    </form>
</div>

<script>
    function showFeedback(qidx, selectedValue, correctAnswer) {
        const fbDiv = document.getElementById('fb' + qidx);
        if (!selectedValue) {
            fbDiv.innerHTML = '<i class="fas fa-exclamation-triangle"></i> No has seleccionado ninguna opción.';
            fbDiv.className = 'feedback incorrect';
            fbDiv.style.display = 'block';
            return;
        }
        if (selectedValue === correctAnswer) {
            fbDiv.innerHTML = '<i class="fas fa-check-circle"></i> ¡Correcto! ' + correctAnswer;
            fbDiv.className = 'feedback correct';
        } else {
            fbDiv.innerHTML = '<i class="fas fa-times-circle"></i> Incorrecto. La respuesta correcta es: ' + correctAnswer;
            fbDiv.className = 'feedback incorrect';
        }
        fbDiv.style.display = 'block';
    }

    // Asignar eventos a cada botón de comprobación
    document.querySelectorAll('.btn-check-ans').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const qidx = btn.getAttribute('data-qidx');
            const correctAnswer = btn.getAttribute('data-correct');
            const selectedRadio = document.querySelector(`input[name="q${qidx}"]:checked`);
            const selectedValue = selectedRadio ? selectedRadio.value : null;
            showFeedback(qidx, selectedValue, correctAnswer);
        });
    });

    // Botón revisar todas
    document.getElementById('checkAllBtn').addEventListener('click', () => {
        document.querySelectorAll('.btn-check-ans').forEach(btn => {
            const qidx = btn.getAttribute('data-qidx');
            const correctAnswer = btn.getAttribute('data-correct');
            const selectedRadio = document.querySelector(`input[name="q${qidx}"]:checked`);
            const selectedValue = selectedRadio ? selectedRadio.value : null;
            showFeedback(qidx, selectedValue, correctAnswer);
        });
    });

    // Botón limpiar respuestas
    document.getElementById('resetBtn').addEventListener('click', () => {
        document.querySelectorAll('input[type="radio"]').forEach(radio => radio.checked = false);
        document.querySelectorAll('.feedback').forEach(fb => fb.style.display = 'none');
    });
</script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
    return html_content

# ------------------------------------------------------------
# 4. Función principal para guardar archivo
# ------------------------------------------------------------
def guardar_examen(tema: str, num_preguntas: int = 10, filename: str = None):
    """Genera el HTML y lo guarda en un archivo."""
    if filename is None:
        filename = f"examen_{tema}_{num_preguntas}preguntas.html"
    html = generar_html_examen(tema, num_preguntas)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Examen generado: {filename}")
    return filename

# ------------------------------------------------------------
# 5. Ejemplo de uso desde línea de comandos
# ------------------------------------------------------------
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generador de ejercicios interactivos de retórica o etimología.")
    parser.add_argument("--tema", choices=["retorica", "etimologia"], default="retorica",
                        help="Temática de los ejercicios")
    parser.add_argument("--preguntas", type=int, default=10,
                        help="Número de preguntas (por defecto 10)")
    parser.add_argument("--salida", type=str, default=None,
                        help="Nombre del archivo HTML de salida")
    args = parser.parse_args()
    
    guardar_examen(args.tema, args.preguntas, args.salida)