#!/usr/bin/env python
import os
import sys
import django
import json
import re
from pathlib import Path

# Configurar Django
sys.path.append('/workspaces/Linguakit-Academy')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linguakit.settings')
django.setup()

from apps.content.models import LinguisticTechnique

# Intentar importar BeautifulSoup
try:
    from bs4 import BeautifulSoup
    BS_AVAILABLE = True
except ImportError:
    BS_AVAILABLE = False
    print("⚠️ BeautifulSoup no disponible. Usando parsing básico.")

def extraer_contenido_html_basico(filepath):
    """Extrae contenido de HTML usando métodos básicos (sin BeautifulSoup)"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Limpiar tags HTML
        content = re.sub(r'<[^>]+>', ' ', content)
        content = re.sub(r'\s+', ' ', content)
        
        sections = {
            'theory': '',
            'example': '',
            'exercise': '',
            'correct_answer': '',
            'description': ''
        }
        
        # Buscar secciones con regex
        patterns = {
            'theory': r'(?:teoría|explicación|concepto)[:\s]*(.*?)(?=(?:ejemplo|ejercicio|practica)|$)',
            'example': r'(?:ejemplo|muestra)[:\s]*(.*?)(?=(?:ejercicio|practica|teoría)|$)',
            'exercise': r'(?:ejercicio|practica|actividad)[:\s]*(.*?)(?=(?:respuesta|solución|correcta)|$)',
            'correct_answer': r'(?:respuesta correcta|solución)[:\s]*(.*?)(?=\n|$)'
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                sections[key] = match.group(1).strip()[:1000]
        
        return sections
        
    except Exception as e:
        print(f'Error parsing HTML: {e}')
        return None

def extraer_contenido_html_bs4(filepath):
    """Extrae contenido de HTML usando BeautifulSoup"""
    if not BS_AVAILABLE:
        return extraer_contenido_html_basico(filepath)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Eliminar scripts y estilos
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        
        sections = {
            'theory': [],
            'example': [],
            'exercise': [],
            'correct_answer': [],
            'description': []
        }
        
        current_section = 'description'
        for line in lines[:200]:  # Limitar líneas
            lower = line.lower()
            if 'teoría' in lower or 'explicación' in lower or 'concepto' in lower:
                current_section = 'theory'
            elif 'ejemplo' in lower or 'muestra' in lower:
                current_section = 'example'
            elif 'ejercicio' in lower or 'practica' in lower or 'actividad' in lower:
                current_section = 'exercise'
            elif 'respuesta' in lower or 'solución' in lower or 'correcta' in lower:
                current_section = 'correct_answer'
            else:
                if len(line) > 10:
                    sections[current_section].append(line)
        
        # Unir y limitar
        for key in sections:
            sections[key] = '\n'.join(sections[key])[:1000]
        
        return sections
        
    except Exception as e:
        print(f'Error con BeautifulSoup: {e}')
        return extraer_contenido_html_basico(filepath)

def extraer_metadata(filename):
    """Extrae metadatos del nombre del archivo"""
    metadata = {
        'category': '',
        'level': '',
        'grade': '',
        'technique_type': '',
        'title': filename.replace('.html', '').replace('.json', '').replace('.txt', '')[:490]
    }
    
    # Categorías
    categorias = {
        'morfosintaxis': 'morfosintaxis',
        'sintaxis': 'sintaxis',
        'semántica': 'semantica',
        'morfología': 'morfologia',
        'ortografía': 'ortografia',
        'fonética': 'fonetica',
        'fonología': 'fonologia',
        'gramática': 'gramatica',
        'retórica': 'retorica',
        'literatura': 'literatura',
        'redacción': 'redaccion',
        'etimología': 'etimologia',
        'puntuación': 'puntuacion',
        'verbos': 'verbos',
        'sustantivos': 'sustantivos',
        'adjetivos': 'adjetivos',
        'conectores': 'conectores',
    }
    
    for key, value in categorias.items():
        if key in filename.lower():
            metadata['category'] = value
            break
    
    # Nivel
    level_match = re.search(r'nivel\s*([A-C][1-3]?)', filename, re.IGNORECASE)
    if level_match:
        metadata['level'] = level_match.group(1).upper()
    
    # Grado
    grade_match = re.search(r'(\d+)[°º]\s*grado', filename, re.IGNORECASE)
    if grade_match:
        metadata['grade'] = f"{grade_match.group(1)}°"
    
    # Tipo
    if 'flashcard' in filename.lower():
        metadata['technique_type'] = 'flashcard'
    elif 'ejercicio' in filename.lower():
        metadata['technique_type'] = 'ejercicio'
    elif 'técnica' in filename.lower():
        metadata['technique_type'] = 'tecnica'
    elif 'json' in filename.lower():
        metadata['technique_type'] = 'json'
    
    return metadata

def importar_archivo(filepath):
    """Importa un archivo a la base de datos"""
    try:
        filename = filepath.name
        metadata = extraer_metadata(filename)
        
        # Verificar si ya existe
        existing = LinguisticTechnique.objects.filter(title=metadata['title'])
        if existing.exists():
            technique = existing.first()
            # Si tiene contenido vacío, intentar actualizar
            if not technique.theory and not technique.exercise_text:
                if filepath.suffix == '.html':
                    sections = extraer_contenido_html_bs4(filepath)
                    if sections:
                        technique.theory = sections.get('theory', '')[:1000]
                        technique.example = sections.get('example', '')[:1000]
                        technique.exercise_text = sections.get('exercise', '')[:1000]
                        technique.correct_answer = sections.get('correct_answer', '')[:1000]
                        technique.save()
                        print(f'🔄 Actualizado: {filename[:50]}...')
                        return
            print(f'⏭️ Ya existe: {filename[:50]}...')
            return
        
        # Procesar según tipo
        if filepath.suffix == '.json':
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if isinstance(data, list):
                    for item in data[:5]:  # Limitar a 5 por archivo para no saturar
                        if item.get('title'):
                            crear_tecnica(item, metadata)
                    print(f'✅ JSON: {filename[:50]}...')
                elif isinstance(data, dict):
                    crear_tecnica(data, metadata)
                    print(f'✅ JSON: {filename[:50]}...')
                return
            except Exception as e:
                print(f'⚠️ JSON error en {filename}: {e}')
        
        # Procesar HTML
        if filepath.suffix == '.html':
            sections = extraer_contenido_html_bs4(filepath)
            technique = LinguisticTechnique.objects.create(
                title=metadata['title'][:490],
                category=metadata.get('category', ''),
                level=metadata.get('level', ''),
                grade=metadata.get('grade', ''),
                technique_type=metadata.get('technique_type', ''),
                theory=sections.get('theory', '')[:1000] if sections else '',
                example=sections.get('example', '')[:1000] if sections else '',
                exercise_text=sections.get('exercise', '')[:1000] if sections else 'Contenido disponible en el archivo original',
                correct_answer=sections.get('correct_answer', '')[:1000] if sections else '',
                content={'filename': filename, 'sections': sections} if sections else {'filename': filename}
            )
            print(f'✅ {filename[:50]}...')
            return
        
        # Si no es HTML ni JSON, solo metadatos
        technique = LinguisticTechnique.objects.create(
            title=metadata['title'][:490],
            category=metadata.get('category', ''),
            level=metadata.get('level', ''),
            grade=metadata.get('grade', ''),
            technique_type=metadata.get('technique_type', 'archivo'),
            content={'filename': filename}
        )
        print(f'📄 {filename[:50]}...')
        
    except Exception as e:
        print(f'❌ Error en {filepath.name}: {str(e)[:100]}')

def crear_tecnica(data, metadata):
    """Crea una técnica desde datos JSON"""
    try:
        title = data.get('title', metadata['title'])
        if len(title) > 490:
            title = title[:487] + '...'
        
        technique = LinguisticTechnique.objects.create(
            title=title,
            category=data.get('category', metadata.get('category', '')),
            level=data.get('level', metadata.get('level', '')),
            grade=data.get('grade', metadata.get('grade', '')),
            technique_type=data.get('type', metadata.get('technique_type', 'json')),
            theory=str(data.get('theory', ''))[:1000],
            example=str(data.get('example', ''))[:1000],
            exercise_text=str(data.get('exercise', data.get('practica', '')))[:1000],
            correct_answer=str(data.get('correct_answer', data.get('respuesta', '')))[:1000],
            content=data,
            points=data.get('points', 10),
            difficulty=data.get('difficulty', 1)
        )
    except Exception as e:
        print(f'❌ Error en JSON item: {e}')

def main():
    """Función principal"""
    path = Path('/workspaces/Linguakit-Academy/apps/api/ejercicios_completos-lengua-castellana')
    
    if not path.exists():
        print(f'❌ Ruta no encontrada: {path}')
        return
    
    files = [f for f in path.iterdir() if f.is_file() and not f.name.startswith('.')]
    total = len(files)
    
    print(f'📂 Encontrados {total} archivos')
    print(f'📊 Técnicas existentes: {LinguisticTechnique.objects.count()}')
    print(f'🔧 BeautifulSoup disponible: {BS_AVAILABLE}')
    print(f'🔄 Comenzando importación...\n')
    
    count = 0
    for filepath in files:
        importar_archivo(filepath)
        count += 1
        if count % 50 == 0:
            print(f'\n📊 Progreso: {count}/{total} | Total en BD: {LinguisticTechnique.objects.count()}\n')
    
    print(f'\n🎉 IMPORTACIÓN COMPLETADA!')
    print(f'📊 Total en BD: {LinguisticTechnique.objects.count()} técnicas')

if __name__ == '__main__':
    main()
