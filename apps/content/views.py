from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.content.models import LinguisticTechnique

def home(request):
    """Página de inicio del sitio"""
    # Estadísticas rápidas
    total_tecnicas = LinguisticTechnique.objects.count()
    total_categorias = LinguisticTechnique.objects.exclude(
        category__isnull=True
    ).exclude(
        category=''
    ).values('category').distinct().count()
    
    # Últimas técnicas agregadas
    ultimas = LinguisticTechnique.objects.all().order_by('-id')[:6]
    
    # Categorías con más técnicas (excluyendo vacías)
    categorias_populares = LinguisticTechnique.objects.exclude(
        category__isnull=True
    ).exclude(
        category=''
    ).values('category').annotate(
        count=Count('id')
    ).order_by('-count')[:6]
    
    context = {
        'total_tecnicas': total_tecnicas,
        'total_categorias': total_categorias,
        'ultimas': ultimas,
        'categorias_populares': categorias_populares,
    }
    return render(request, 'content/home.html', context)

def index(request):
    """Vista principal del índice de contenido"""
    tecnicas = LinguisticTechnique.objects.all().order_by('category', 'title')
    
    # Paginación
    paginator = Paginator(tecnicas, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estadísticas
    total = tecnicas.count()
    categorias = LinguisticTechnique.objects.exclude(
        category__isnull=True
    ).exclude(
        category=''
    ).values('category').annotate(
        count=Count('id')
    ).order_by('category')
    
    niveles = LinguisticTechnique.objects.values('level').annotate(
        count=Count('id')
    ).order_by('level')
    
    # Últimas técnicas agregadas
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
    """Técnicas por categoría"""
    if not categoria:
        return redirect('content:index')
    
    tecnicas = LinguisticTechnique.objects.filter(category=categoria).order_by('title')
    
    paginator = Paginator(tecnicas, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categoria': categoria,
        'total': tecnicas.count(),
        'titulo': f'Técnicas de {categoria}',
    }
    return render(request, 'content/lista.html', context)

def por_nivel(request, nivel):
    """Técnicas por nivel educativo"""
    tecnicas = LinguisticTechnique.objects.filter(level=nivel).order_by('title')
    
    paginator = Paginator(tecnicas, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'nivel': nivel,
        'total': tecnicas.count(),
        'titulo': f'Técnicas Nivel {nivel}',
    }
    return render(request, 'content/lista.html', context)

def detalle(request, id):
    """Vista de detalle de una técnica"""
    tecnica = get_object_or_404(LinguisticTechnique, id=id)
    
    # Técnicas relacionadas (misma categoría)
    relacionadas = LinguisticTechnique.objects.filter(
        category=tecnica.category
    ).exclude(id=tecnica.id)[:5] if tecnica.category else []
    
    context = {
        'tecnica': tecnica,
        'relacionadas': relacionadas,
    }
    return render(request, 'content/detalle.html', context)

def buscar(request):
    """Búsqueda de técnicas"""
    query = request.GET.get('q', '')
    resultados = []
    
    if query:
        resultados = LinguisticTechnique.objects.filter(
            Q(title__icontains=query) |
            Q(theory__icontains=query) |
            Q(exercise_text__icontains=query)
        ).order_by('title')
    
    context = {
        'query': query,
        'resultados': resultados,
        'total': resultados.count(),
    }
    return render(request, 'content/buscar.html', context)

# Vistas para el dashboard (requieren login)
@login_required
def dashboard_estudiante(request):
    """Dashboard del estudiante"""
    total = LinguisticTechnique.objects.count()
    context = {
        'total_tecnicas': total,
        'ultimas_tecnicas': LinguisticTechnique.objects.all().order_by('-id')[:10],
        'categorias_stats': LinguisticTechnique.objects.exclude(
            category__isnull=True
        ).exclude(
            category=''
        ).values('category').annotate(
            count=Count('id')
        ).order_by('-count')[:10],
    }
    return render(request, 'content/dashboard_estudiante.html', context)

@login_required
def dashboard_profesor(request):
    """Dashboard del profesor"""
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('content:index')
    
    total = LinguisticTechnique.objects.count()
    context = {
        'total_tecnicas': total,
        'categorias_stats': LinguisticTechnique.objects.exclude(
            category__isnull=True
        ).exclude(
            category=''
        ).values('category').annotate(
            count=Count('id')
        ).order_by('category'),
        'niveles_stats': LinguisticTechnique.objects.values('level').annotate(
            count=Count('id')
        ).order_by('level'),
        'ultimas_tecnicas': LinguisticTechnique.objects.all().order_by('-id')[:15],
    }
    return render(request, 'content/dashboard_profesor.html', context)
