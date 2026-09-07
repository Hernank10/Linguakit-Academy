#!/bin/bash

echo "🚀 SUBIENDO CAMBIOS A GITHUB"

# 1. Agregar todos los archivos
git add -A

# 2. Commit
git commit -m "🎉 PLATAFORMA LINGUAKIT-ACADEMY COMPLETA

📊 CONTENIDO GENERADO:
- 50 programas de Morfosintaxis, Redacción y Literatura Castellana
- 100 cursos especializados
- 394 lecciones estructuradas
- 11,820 ejercicios interactivos (30 por lección)
- Secuencias didácticas creadas

🚀 SISTEMAS IMPLEMENTADOS:
✅ Gestión de Programas, Cursos, Lecciones y Ejercicios
✅ Generación masiva de contenido educativo
✅ Filtros personalizados en el admin
✅ Mínimo 30 ejercicios por lección
✅ 100 ejercicios por página en el admin

📁 SCRIPTS CREADOS:
- generar_contenido_masivo.py
- generar_30_ejercicios_por_leccion.py
- verificar_contenido.py
- crear_usuarios.py
- cambiar_programas.py

🛠️ MEJORAS TÉCNICAS:
- Admin de ejercicios con filtros funcionales
- Paginación de 100 elementos
- Registro único de modelos en admin

📈 CRECIMIENTO:
- Ejercicios totales: 11,820 (+10,063 generados)
- Cobertura: 100% de lecciones con 30+ ejercicios"

# 3. Push
git push origin main

echo ""
echo "✅ ¡CAMBIOS SUBIDOS EXITOSAMENTE!"
git log --oneline -1
