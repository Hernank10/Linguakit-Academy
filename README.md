# 🎓 Linguakit Academy - LMS Inteligente

Linguakit Academy es una plataforma de gestión de aprendizaje (LMS) diseñada para la enseñanza de **Lingüística (Redacción)** y **Programación**. El sistema permite a los estudiantes practicar gramática y código en tiempo real con validación automática.

## 🚀 Características Principales

* **Sistema de Niveles:** Cursos organizados desde **A1 hasta B2**.
* **Editor de Código Integrado:** Uso de **Ace Editor** (Monokai Theme) para prácticas de Python.
* **Gamificación:** Efectos visuales de éxito con **Canvas Confetti**.
* **Dashboard del Estudiante:** Panel personalizado para gestionar cursos matriculados y oferta académica.
* **Gestión Administrativa:** Panel de control para que los profesores gestionen programas, lecciones y secuencias didácticas.

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python 3.12 + Django 6.0
* **Frontend:** Bootstrap 5, Javascript (AJAX), Ace Editor
* **Base de Datos:** SQLite (Desarrollo)
* **Manejo de Imágenes:** Pillow

## 📥 Instalación y Configuración

Si deseas clonar este proyecto y ejecutarlo localmente:

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Hernank10/Linguakit-Academy.git
   cd Linguakit-Academy
   ```

2. **Crear y activar el entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar migraciones y servidor:**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

## 📂 Estructura del Proyecto

* `apps/core`: Gestión de programas, niveles y matrículas.
* `apps/cursos`: Lecciones, ejercicios y motor de validación.
* `apps/contenidos`: Secuencias didácticas y objetivos pedagógicos.
* `apps/usuarios`: Perfiles, autenticación y dashboards.

---
Desarrollado por **@Hernank10** - 2026.
