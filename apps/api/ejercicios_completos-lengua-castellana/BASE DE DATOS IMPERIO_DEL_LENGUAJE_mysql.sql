-- ============================================================
-- BASE DE DATOS: IMPERIO_DEL_LENGUAJE
-- ============================================================
CREATE DATABASE IF NOT EXISTS ImperioDelLenguaje;
USE ImperioDelLenguaje;

-- ============================================================
-- 1. TABLA: USUARIOS
-- ============================================================
CREATE TABLE Usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    ultimo_acceso DATETIME DEFAULT NULL,
    activo BOOLEAN DEFAULT TRUE
);

-- ============================================================
-- 2. TABLA: APLICACIONES (Las 5 apps que hicimos)
-- ============================================================
CREATE TABLE Aplicaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,      -- Ej: 'Gramatical', 'Sintáctica', 'Mecánica', 'Solar', 'Automotriz'
    descripcion TEXT,
    icono VARCHAR(50),                       -- Ej: '📚', '🏛️', '⚡', '☀️', '🚗'
    color_hex VARCHAR(7),                    -- Ej: '#ffd54f'
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 3. TABLA: MODULOS (Las Amazonas / Categorías dentro de cada app)
-- ============================================================
CREATE TABLE Modulos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    aplicacion_id INT NOT NULL,
    nombre VARCHAR(50) NOT NULL,             -- Ej: 'Morfema', 'Sujeto', 'Motorcar'
    descripcion TEXT,
    color_hex VARCHAR(7),                    -- Color del módulo dentro de la app
    orden TINYINT DEFAULT 0,                 -- Para ordenar visualmente
    FOREIGN KEY (aplicacion_id) REFERENCES Aplicaciones(id) ON DELETE CASCADE
);

-- ============================================================
-- 4. TABLA: TECNICAS (100 técnicas por app = 500 en total)
-- ============================================================
CREATE TABLE Tecnicas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    modulo_id INT NOT NULL,
    numero_tecnica TINYINT NOT NULL,         -- Número 1-20 dentro del módulo
    titulo VARCHAR(100) NOT NULL,
    teoria TEXT NOT NULL,
    ejemplo TEXT NOT NULL,
    ejercicio TEXT NOT NULL,
    reto TEXT NOT NULL,
    -- Campos extras para orden y metadatos
    nivel_dificultad TINYINT DEFAULT 1,      -- 1=Inicial, 2=Intermedio, 3=Avanzado
    palabras_clave VARCHAR(255),              -- Para búsquedas
    FOREIGN KEY (modulo_id) REFERENCES Modulos(id) ON DELETE CASCADE,
    UNIQUE KEY (modulo_id, numero_tecnica)    -- Evita duplicados
);

-- ============================================================
-- 5. TABLA: PROGRESO_USUARIO (Seguimiento de técnicas completadas)
-- ============================================================
CREATE TABLE ProgresoUsuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    tecnica_id INT NOT NULL,
    completado BOOLEAN DEFAULT FALSE,
    fecha_inicio DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_completado DATETIME DEFAULT NULL,
    -- Para almacenar respuestas de ejercicios (opcional)
    respuesta_usuario TEXT DEFAULT NULL,
    -- Para saber si la respuesta fue validada (en caso de ejercicios)
    validado BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (tecnica_id) REFERENCES Tecnicas(id) ON DELETE CASCADE,
    UNIQUE KEY (usuario_id, tecnica_id)       -- Un registro por usuario-técnica
);

-- ============================================================
-- 6. TABLA: FLASHCARDS (Para el sistema de repaso, extraíble de las técnicas)
-- ============================================================
CREATE TABLE Flashcards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tecnica_id INT NOT NULL,
    pregunta VARCHAR(255) NOT NULL,           -- Puede ser el título de la técnica
    respuesta TEXT NOT NULL,                  -- Puede ser la teoría de la técnica
    FOREIGN KEY (tecnica_id) REFERENCES Tecnicas(id) ON DELETE CASCADE
);
-- Nota: En la app, los flashcards se generaban automáticamente desde las técnicas.
-- Esta tabla permite tener versiones personalizadas si se requiere.

-- ============================================================
-- 7. VISTA: VW_PROGRESO_GENERAL (Reporte rápido de avance)
-- ============================================================
CREATE VIEW Vw_ProgresoGeneral AS
SELECT 
    u.id AS usuario_id,
    u.nombre AS usuario_nombre,
    COUNT(DISTINCT t.id) AS total_tecnicas,
    SUM(CASE WHEN pu.completado = TRUE THEN 1 ELSE 0 END) AS completadas,
    ROUND((SUM(CASE WHEN pu.completado = TRUE THEN 1 ELSE 0 END) / COUNT(DISTINCT t.id)) * 100, 2) AS porcentaje
FROM Usuarios u
CROSS JOIN Tecnicas t
LEFT JOIN ProgresoUsuario pu ON pu.usuario_id = u.id AND pu.tecnica_id = t.id
GROUP BY u.id, u.nombre;