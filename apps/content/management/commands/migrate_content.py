import os
import json
import re
from pathlib import Path
from django.core.management.base import BaseCommand
from apps.content.models import LinguisticTechnique

class Command(BaseCommand):
    help = 'Migra contenido de archivos HTML/JSON a la base de datos'
    
    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help='Ruta a los archivos')
        parser.add_argument('--limit', type=int, help='Límite de archivos a procesar')
        parser.add_argument('--clear', action='store_true', help='Limpiar datos existentes')
    
    def handle(self, *args, **options):
        path = options.get('path', 'apps/api/ejercicios_completos-lengua-castellana')
        limit = options.get('limit', None)
        clear = options.get('clear', False)
        
        if clear:
            count = LinguisticTechnique.objects.count()
            LinguisticTechnique.objects.all().delete()
            self.stdout.write(f'🗑️ Eliminados {count} registros existentes')
        
        base_dir = Path(path)
        
        if not base_dir.exists():
            self.stdout.write(self.style.ERROR(f'❌ Ruta no encontrada: {path}'))
            self.stdout.write(self.style.WARNING(f'📂 Buscando en directorio actual: {os.getcwd()}'))
            return
        
        files = [f for f in base_dir.iterdir() if f.is_file() and not f.name.startswith('.')]
        total = len(files)
        
        if limit:
            files = files[:limit]
        
        self.stdout.write(f'📂 Procesando {len(files)} archivos de {total} totales...')
        
        count = 0
        errors = 0
        
        for filepath in files:
            try:
                self.process_file(filepath)
                count += 1
                self.stdout.write(f'✅ {filepath.name[:60]}...')
            except Exception as e:
                errors += 1
                self.stdout.write(self.style.ERROR(f'❌ Error en {filepath.name}: {e}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n🎉 Migración completada: {count} archivos procesados, {errors} errores'))
        self.stdout.write(f'📊 Total en BD: {LinguisticTechnique.objects.count()} técnicas')
    
    def process_file(self, filepath):
        """Procesa un archivo individual"""
        filename = filepath.name
        metadata = self.extract_metadata(filename)
        
        if filepath.suffix == '.json':
            self.process_json(filepath, metadata)
        else:
            self.process_html(filepath, metadata)
    
    def extract_metadata(self, filename):
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
        elif 'técnica' in filename.lower():
            metadata['technique_type'] = 'tecnica'
        
        return metadata
    
    def process_json(self, filepath, metadata):
        """Procesa archivo JSON"""
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except:
                return
        
        if isinstance(data, list):
            for item in data:
                self.create_technique(item, metadata)
        elif isinstance(data, dict):
            self.create_technique(data, metadata)
    
    def process_html(self, filepath, metadata):
        """Procesa archivo HTML"""
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
        
        technique = LinguisticTechnique.objects.create(
            title=metadata['title'],
            category=metadata.get('category', ''),
            level=metadata.get('level', ''),
            grade=metadata.get('grade', ''),
            technique_type=metadata.get('technique_type', ''),
            theory=sections['theory'],
            example=sections['example'],
            exercise=sections['exercise'],
            correct_answer=sections['correct_answer'],
            content={'sections': sections, 'metadata': metadata}
        )
        
        return technique
    
    def create_technique(self, data, metadata):
        """Crea una técnica desde datos JSON"""
        technique = LinguisticTechnique.objects.create(
            title=data.get('title', metadata['title'][:490]),
            category=data.get('category', metadata.get('category', '')),
            level=data.get('level', metadata.get('level', '')),
            grade=data.get('grade', metadata.get('grade', '')),
            technique_type=data.get('type', metadata.get('technique_type', '')),
            theory=data.get('theory', ''),
            example=data.get('example', ''),
            exercise=data.get('exercise', ''),
            correct_answer=data.get('correct_answer', ''),
            content=data,
            points=data.get('points', 10),
            difficulty=data.get('difficulty', 1)
        )
        return technique
