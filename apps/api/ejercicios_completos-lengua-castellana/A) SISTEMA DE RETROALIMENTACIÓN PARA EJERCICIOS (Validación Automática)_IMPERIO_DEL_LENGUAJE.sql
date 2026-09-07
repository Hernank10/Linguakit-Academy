-- ============================================================
-- SISTEMA DE RETROALIMENTACIÓN - TABLAS
-- ============================================================

-- 1.1 Añadir campo de respuesta esperada a Tecnicas
ALTER TABLE Tecnicas ADD COLUMN respuesta_esperada TEXT DEFAULT NULL;
ALTER TABLE Tecnicas ADD COLUMN tipo_ejercicio ENUM('texto', 'opcion_multiple', 'verdadero_falso') DEFAULT 'texto';

-- 1.2 Tabla de opciones múltiples (para ejercicios tipo quiz)
CREATE TABLE OpcionesEjercicio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tecnica_id INT NOT NULL,
    opcion TEXT NOT NULL,
    es_correcta BOOLEAN DEFAULT FALSE,
    orden TINYINT DEFAULT 0,
    FOREIGN KEY (tecnica_id) REFERENCES Tecnicas(id) ON DELETE CASCADE
);

-- 1.3 Tabla de intentos de ejercicios
CREATE TABLE IntentosEjercicio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    tecnica_id INT NOT NULL,
    respuesta_usuario TEXT,
    es_correcto BOOLEAN DEFAULT FALSE,
    puntaje_obtenido INT DEFAULT 0,
    fecha_intento DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (tecnica_id) REFERENCES Tecnicas(id) ON DELETE CASCADE
);

-- 1.4 Tabla de retroalimentación (feedback personalizado)
CREATE TABLE RetroalimentacionEjercicio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tecnica_id INT NOT NULL,
    criterio VARCHAR(100) NOT NULL,
    mensaje TEXT NOT NULL,
    FOREIGN KEY (tecnica_id) REFERENCES Tecnicas(id) ON DELETE CASCADE
);