from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Leccion, Ejercicio
import json

def leccion_detalle(request, leccion_id):
    leccion = get_object_or_404(Leccion, id=leccion_id)
    secuencia = getattr(leccion.programa, 'secuencia', None)
    return render(request, 'cursos/leccion_detalle.html', {
        'leccion': leccion,
        'secuencia': secuencia
    })

def validar_ejercicio(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # Aquí recibimos el código del Ace Editor
            return JsonResponse({
                "correcto": True, 
                "mensaje": "¡Excelente trabajo! Has superado este desafío. 🎉"
            })
        except Exception as e:
            return JsonResponse({"correcto": False, "mensaje": str(e)})
    return JsonResponse({"error": "Método no permitido"}, status=405)
