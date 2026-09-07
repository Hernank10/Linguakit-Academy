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

def extract_metadata(filename):
    """Extrae metadatos del nombre del archivo"""
    metadata = {
        'category': '',
        'level': '',
        'grade': '',
        'technique_type': '',
        'title': filename.replace('.html', '').replace('.json', '').replace('.txt', '')[:490]
    }
    
    categories = {
        'morfosintaxis': 'morfosintaxis',
        'sintaxis': 'sintaxis',
        'semantica': 'semantica',
        'morfologia': 'morfologia',
        'ortografia': 'ortografia',
        'fonetica': 'fonetica',
        'fonologia': 'fonologia',
        'gramatica': 'gramatica',
        'retorica': 'retorica',
        'literatura': 'literatura',
        'redaccion': 'redaccion',
        'etimologia': 'etimologia',
        'puntuacion': 'puntuacion',
    }
    
    for key, value in categories.items():
        if key in filename.lower():
            metadata['category'] = value
            break
    
    level_match = re.search(r'nivel\s*([A-C][1-3]?)', filename, re.IGNORECASE)
    if level_match:
        metadata['level'] = level_match.group(1).upper()
    
    grade_match = re.search(r'(\d+)[°º]\s*grado', filename, re.IGNORECASE)
    if grade_match:
        metadata['grade'] = f"{grade_match.group(1)}°"
    
    if 'flashcard' in filename.lower():
        metadata['technique_type'] = 'flashcard'
    elif 'ejercicio' in filename.lower():
        metadata['technique_type'] = 'ejercicio'
    elif 'tecnica' in filename.lower():
        metadata['technique_type'] = 'tecnica'
    
    return metadata

def parse_html_content(filepath):
    """Extrae contenido de archivos HTML"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    sections = {
        'theory': '',
        'example': '',
        'exercise': '',
        'correct_answer': ''
    }
    
    patterns = {
        'theory': r'(?:teoría|explicación|concepto)[:\s]*(.*?)(?=\n(?:ejemplo|ejercicio|practica)|$)',
        'example': r'(?:ejemplo|muestra)[:\s]*(.*?)(?=\n(?:ejercicio|practica|teoría)|$)',
        'exercise': r'(?:ejercicio|practica|actividad)[:\s]*(.*?)(?=\n(?:respuesta|solución|correcta)|$)',
        'correct_answer': r'(?:respuesta correcta|solución)[:\s]*(.*?)(?=\n|$)'
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        if match:
            sections[key] = match.group(1).strip()
    
    return sections

def importar_archivo(filepath):
    """Importa un archivo individual"""
    try:
        filename = filepath.name
        metadata = extract_metadata(filename)
        
        # Verificar si ya existe
        if LinguisticTechnique.objects.filter(title=metadata['title']).exists():
            print(f'⏭️ Ya existe: {filename[:50]}...')
            return
        
        if filepath.suffix == '.json':
            with open(filepath, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list):
                        for item in data:
                            crear_tecnica(item, metadata)
                    elif isinstance(data, dict):
                        crear_tecnica(data, metadata)
                    return
                except:
                    pass
        
        # Procesar como HTML
        sections = parse_html_content(filepath)
        
        technique = LinguisticTechnique.objects.create(
            title=metadata['title'],
            category=metadata.get('category', ''),
            level=metadata.get('level', ''),
            grade=metadata.get('grade', ''),
            technique_type=metadata.get('technique_type', ''),
            theory=sections['theory'],
            example=sections['example'],
            exercise_text=sections['exercise'],
            correct_answer=sections['correct_answer'],
            content={'sections': sections, 'metadata': metadata, 'filename': filename}
        )
        print(f'✅ {filename[:50]}...')
        
    except Exception as e:
        print(f'❌ Error en {filepath.name}: {e}')

def crear_tecnica(data, metadata):
    """Crea una técnica desde datos JSON"""
    try:
        technique = LinguisticTechnique.objects.create(
            title=data.get('title', metadata['title'][:490]),
            category=data.get('category', metadata.get('category', '')),
            level=data.get('level', metadata.get('level', '')),
            grade=data.get('grade', metadata.get('grade', '')),
            technique_type=data.get('type', metadata.get('technique_type', '')),
            theory=data.get('theory', ''),
            example=data.get('example', ''),
            exercise_text=data.get('exercise', ''),
            correct_answer=data.get('correct_answer', ''),
            content=data,
            points=data.get('points', 10),
            difficulty=data.get('difficulty', 1)
        )
        print(f'✅ JSON: {data.get("title", metadata["title"])[:50]}...')
    except Exception as e:
        print(f'❌ Error en JSON: {e}')

def main():
    """Función principal"""
    path = Path('/workspaces/Linguakit-Academy/apps/api/ejercicios_completos-lengua-castellana')
    
    if not path.exists():
        print(f'❌ Ruta no encontrada: {path}')
        return
    
    files = list(path.iterdir())
    total = len(files)
    
    print(f'📂 Encontrados {total} archivos')
    print(f'📊 Técnicas existentes: {LinguisticTechnique.objects.count()}')
    
    # Limpiar datos existentes (opcional)
    # LinguisticTechnique.objects.all().delete()
    # print('🗑️ Datos limpiados')
    
    count = 0
    for filepath in files:
        if filepath.is_file() and not filepath.name.startswith('.'):
            importar_archivo(filepath)
            count += 1
            if count % 10 == 0:
                print(f'📊 Progreso: {count}/{total}')
    
    print(f'\n🎉 IMPORTACIÓN COMPLETADA!')
    print(f'📊 Total en BD: {LinguisticTechnique.objects.count()} técnicas')

if __name__ == '__main__':
    main()
