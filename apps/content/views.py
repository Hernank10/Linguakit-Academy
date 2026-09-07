from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.content.models import LinguisticTechnique, Curso, Leccion, Ejercicio, Evaluacion

def home(request):
    """Página de inicio del sitio"""
    total_tecnicas = LinguisticTechnique.objects.count()
    total_categorias = LinguisticTechnique.objects.exclude(category__isnull=True).exclude(category='').values('category').distinct().count()
    total_cursos = Curso.objects.count()
    
    ultimas = LinguisticTechnique.objects.all().order_by('-id')[:6]
    categorias_populares = LinguisticTechnique.objects.exclude(category__isnull=True).exclude(category='').values('category').annotate(count=Count('id')).order_by('-count')[:6]
    ultimos_cursos = Curso.objects.all().order_by('-id')[:4]
    
    context = {
        'total_tecnicas': total_tecnicas,
        'total_categorias': total_categorias,
        'total_cursos': total_cursos,
        'ultimas': ultimas,
        'categorias_populares': categorias_populares,
        'ultimos_cursos': ultimos_cursos,
    }
    return render(request, 'content/home.html', context)

def index(request):
    """Vista principal del índice de contenido"""
    tecnicas = LinguisticTechnique.objects.all().order_by('category', 'title')
    
    paginator = Paginator(tecnicas, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    total = tecnicas.count()
    categorias = LinguisticTechnique.objects.exclude(category__isnull=True).exclude(category='').values('category').annotate(count=Count('id')).order_by('category')
    niveles = LinguisticTechnique.objects.values('level').annotate(count=Count('id')).order_by('level')
    ultimas = LinguisticTechnique.objects.all().order_by('-id')[:5]
    
    context = {
        'page_obj': page_obj,
        'total': total,
        'categorias': categorias,
        'niveles': niveles,
        'ultimas': ultimas,
    }
    return render(request, 'content/index.html', context)

def por_categoria(request, categoria):
    if not categoria:
        return redirect('content:index')
    tecnicas = LinguisticTechnique.objects.filter(category=categoria).order_by('title')
    paginator = Paginator(tecnicas, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'categoria': categoria, 'total': tecnicas.count(), 'titulo': f'Técnicas de {categoria}'}
    return render(request, 'content/lista.html', context)

def por_nivel(request, nivel):
    tecnicas = LinguisticTechnique.objects.filter(level=nivel).order_by('title')
    paginator = Paginator(tecnicas, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'nivel': nivel, 'total': tecnicas.count(), 'titulo': f'Técnicas Nivel {nivel}'}
    return render(request, 'content/lista.html', context)

def detalle_tecnica(request, id):
    tecnica = get_object_or_404(LinguisticTechnique, id=id)
    relacionadas = LinguisticTechnique.objects.filter(category=tecnica.category).exclude(id=tecnica.id)[:5] if tecnica.category else []
    context = {'tecnica': tecnica, 'relacionadas': relacionadas}
    return render(request, 'content/detalle_tecnica.html', context)

def buscar(request):
    query = request.GET.get('q', '')
    resultados = []
    if query:
        resultados = list(LinguisticTechnique.objects.filter(
            Q(title__icontains=query) |
            Q(theory__icontains=query) |
            Q(exercise_text__icontains=query)
        ).order_by('title'))
    context = {'query': query, 'resultados': resultados, 'total': len(resultados)}
    return render(request, 'content/buscar.html', context)

def listar_cursos(request):
    cursos = Curso.objects.all().order_by('categoria', 'titulo')
    paginator = Paginator(cursos, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'total': cursos.count()}
    return render(request, 'content/cursos_lista.html', context)

def detalle_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    lecciones = curso.lecciones.all().order_by('orden')
    evaluacion = Evaluacion.objects.filter(curso=curso).first()
    context = {'curso': curso, 'lecciones': lecciones, 'evaluacion': evaluacion}
    return render(request, 'content/curso_detalle.html', context)

def detalle_leccion(request, leccion_id):
    leccion = get_object_or_404(Leccion, id=leccion_id)
    ejercicios = leccion.ejercicios.all()
    context = {'leccion': leccion, 'ejercicios': ejercicios}
    return render(request, 'content/leccion_detalle.html', context)

def detalle_ejercicio(request, ejercicio_id):
    ejercicio = get_object_or_404(Ejercicio, id=ejercicio_id)
    context = {'ejercicio': ejercicio}
    return render(request, 'content/ejercicio_detalle.html', context)

@login_required
def dashboard_estudiante(request):
    usuario = request.user
    cursos = Curso.objects.all()
    total_cursos = cursos.count()
    total_lecciones = Leccion.objects.count()
    total_ejercicios = Ejercicio.objects.count()
    ultimos_cursos = cursos.order_by('-id')[:6]
    context = {
        'usuario': usuario,
        'total_cursos': total_cursos,
        'total_lecciones': total_lecciones,
        'total_ejercicios': total_ejercicios,
        'ultimos_cursos': ultimos_cursos,
        'cursos': cursos,
    }
    return render(request, 'content/dashboard_estudiante.html', context)

@login_required
def dashboard_profesor(request):
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('content:index')
    total_cursos = Curso.objects.count()
    total_lecciones = Leccion.objects.count()
    total_ejercicios = Ejercicio.objects.count()
    total_evaluaciones = Evaluacion.objects.count()
    cursos_categoria = Curso.objects.values('categoria').annotate(count=Count('id')).order_by('-count')
    context = {
        'total_cursos': total_cursos,
        'total_lecciones': total_lecciones,
        'total_ejercicios': total_ejercicios,
        'total_evaluaciones': total_evaluaciones,
        'cursos_categoria': cursos_categoria,
        'ultimos_cursos': Curso.objects.all().order_by('-id')[:10],
    }
    return render(request, 'content/dashboard_profesor.html', context)
