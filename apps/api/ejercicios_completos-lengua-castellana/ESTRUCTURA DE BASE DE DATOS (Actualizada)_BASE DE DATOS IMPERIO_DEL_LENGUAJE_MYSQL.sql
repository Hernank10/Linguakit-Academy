-- ============================================================
-- SISTEMA DE GAMIFICACIÓN - TABLAS COMPLETAS
-- ============================================================

-- 1.1 Tabla de niveles (XP requeridos)
CREATE TABLE Niveles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nivel INT NOT NULL UNIQUE,
    puntos_requeridos INT NOT NULL,          -- Puntos acumulados para alcanzar este nivel
    titulo VARCHAR(50) NOT NULL,
    icono VARCHAR(10) DEFAULT '🏆',
    descripcion TEXT,
    recompensa VARCHAR(100)                  -- Ej: 'Desbloqueas nuevas técnicas'
);

-- Insertar niveles base (del 1 al 20)
INSERT INTO Niveles (nivel, puntos_requeridos, titulo, icono, descripcion) VALUES
(1, 0, 'Novato', '🌱', 'Comienza tu viaje en el imperio del lenguaje'),
(2, 100, 'Aprendiz', '📖', 'Has dado tus primeros pasos'),
(3, 250, 'Estudioso', '✍️', 'La disciplina te define'),
(4, 500, 'Gramático', '📝', 'Empiezas a dominar las reglas'),
(5, 800, 'Sintáctico', '🏛️', 'La estructura de la oración te obedece'),
(6, 1200, 'Orador', '🎙️', 'Tus palabras tienen peso'),
(7, 1700, 'Retórico', '🗡️', 'Persuades con facilidad'),
(8, 2300, 'Filólogo', '📜', 'El amor por el lenguaje te guía'),
(9, 3000, 'Sabio', '🧙', 'La sabiduría te acompaña'),
(10, 4000, 'Maestro', '🏅', 'Eres un referente'),
(11, 5200, 'Arquitecto del Verbo', '🏗️', 'Construyes mundos con palabras'),
(12, 6600, 'Guardian del Lenguaje', '🛡️', 'Proteges la lengua'),
(13, 8200, 'Cronista', '📖', 'Registras la historia'),
(14, 10000, 'Senador', '🏛️', 'Tienes voz en el imperio'),
(15, 12000, 'Cónsul', '⚖️', 'Administras el saber'),
(16, 14500, 'Legado', '📜', 'Dejas huella'),
(17, 17500, 'Prefecto', '⭐', 'Gobiernas el conocimiento'),
(18, 21000, 'Imperator', '👑', 'El poder del lenguaje te pertenece'),
(19, 25000, 'Dios del Verbo', '✨', 'Has alcanzado la cima'),
(20, 30000, 'Leyenda Viviente', '🔥', 'Tu nombre será recordado por siempre');

-- 1.2 Tabla de logros
CREATE TABLE Logros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT,
    icono VARCHAR(10) DEFAULT '🎖️',
    puntos_recompensa INT DEFAULT 50,        -- Puntos extra por desbloquear
    criterio_tipo ENUM('tecnicas', 'racha', 'dias', 'especial') NOT NULL,
    criterio_valor VARCHAR(100) NOT NULL,    -- Ej: '50', '7', 'completar_todas'
    categoria VARCHAR(50) DEFAULT 'general'
);

-- Insertar logros base
INSERT INTO Logros (nombre, descripcion, icono, puntos_recompensa, criterio_tipo, criterio_valor, categoria) VALUES
('Primer paso', 'Completa tu primera técnica', '🌟', 10, 'tecnicas', '1', 'progreso'),
('10 técnicas', 'Completa 10 técnicas', '📚', 25, 'tecnicas', '10', 'progreso'),
('25 técnicas', 'Completa 25 técnicas', '📖', 50, 'tecnicas', '25', 'progreso'),
('50 técnicas', 'Completa 50 técnicas', '🏛️', 100, 'tecnicas', '50', 'progreso'),
('75 técnicas', 'Completa 75 técnicas', '📜', 150, 'tecnicas', '75', 'progreso'),
('Maestro del lenguaje', 'Completa todas las 100 técnicas', '👑', 250, 'tecnicas', '100', 'progreso'),
('Racha de 7 días', 'Mantén una racha de 7 días seguidos', '🔥', 50, 'racha', '7', 'racha'),
('Racha de 14 días', 'Mantén una racha de 14 días seguidos', '⚡', 100, 'racha', '14', 'racha'),
('Racha de 30 días', 'Mantén una racha de 30 días seguidos', '💎', 200, 'racha', '30', 'racha'),
('Semana completa', 'Completa técnicas durante 7 días consecutivos', '📅', 75, 'dias', '7', 'racha'),
('Mes completo', 'Completa técnicas durante 30 días consecutivos', '🌟', 150, 'dias', '30', 'racha'),
('Gramática básica', 'Completa todas las técnicas de Morfema', '📝', 50, 'especial', 'morfema', 'especial'),
('Sintaxis dominada', 'Completa todas las técnicas de Sintaxis', '🏛️', 50, 'especial', 'sintaxis', 'especial'),
('Ortografía impecable', 'Completa todas las técnicas de Ortografía', '✍️', 50, 'especial', 'ortografia', 'especial'),
('Fonética experta', 'Completa todas las técnicas de Fonética', '🎙️', 50, 'especial', 'fonetica', 'especial'),
('Semántica avanzada', 'Completa todas las técnicas de Semántica', '📖', 50, 'especial', 'semantica', 'especial'),
('Mecánica básica', 'Completa todas las técnicas de Motorio', '⚙️', 50, 'especial', 'motorio', 'especial');

-- 1.3 Tabla de puntos y nivel del usuario
CREATE TABLE PuntosUsuario (
    usuario_id INT NOT NULL,
    puntos INT DEFAULT 0,
    nivel_actual INT DEFAULT 1,
    racha_actual INT DEFAULT 0,
    mejor_racha INT DEFAULT 0,
    ultimo_estudio DATETIME DEFAULT NULL,
    total_tecnicas_completadas INT DEFAULT 0,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (nivel_actual) REFERENCES Niveles(nivel) ON DELETE SET NULL
);

-- 1.4 Tabla de logros desbloqueados por usuario
CREATE TABLE LogrosUsuario (
    usuario_id INT NOT NULL,
    logro_id INT NOT NULL,
    fecha_desbloqueo DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (logro_id) REFERENCES Logros(id) ON DELETE CASCADE,
    UNIQUE KEY (usuario_id, logro_id)
);

-- 1.5 Tabla de historial de puntos (para tracking y auditoría)
CREATE TABLE HistorialPuntos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    puntos INT NOT NULL,
    motivo VARCHAR(100) NOT NULL,            -- Ej: 'completar_tecnica', 'logro', 'racha'
    referencia_id INT DEFAULT NULL,          -- ID de la técnica o logro relacionado
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id) ON DELETE CASCADE
);

-- 1.6 Vista: Ranking de usuarios
CREATE VIEW Vw_Ranking AS
SELECT 
    u.id AS usuario_id,
    u.nombre AS usuario_nombre,
    pu.puntos,
    pu.nivel_actual,
    n.titulo AS nivel_titulo,
    n.icono AS nivel_icono,
    pu.total_tecnicas_completadas,
    pu.racha_actual,
    pu.mejor_racha,
    (SELECT COUNT(*) FROM LogrosUsuario lu WHERE lu.usuario_id = u.id) AS logros_desbloqueados
FROM Usuarios u
JOIN PuntosUsuario pu ON pu.usuario_id = u.id
JOIN Niveles n ON n.nivel = pu.nivel_actual
WHERE u.activo = TRUE
ORDER BY pu.puntos DESC, pu.total_tecnicas_completadas DESC;