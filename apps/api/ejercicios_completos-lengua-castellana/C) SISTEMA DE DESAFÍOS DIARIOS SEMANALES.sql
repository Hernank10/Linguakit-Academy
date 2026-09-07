-- ============================================================
-- SISTEMA DE DESAFÍOS
-- ============================================================

-- Tabla de desafíos
CREATE TABLE Desafios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    descripcion TEXT,
    tipo ENUM('diario', 'semanal', 'especial') NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    objetivo INT NOT NULL,                    -- Número de técnicas a completar
    puntos_recompensa INT DEFAULT 50,
    logro_id INT DEFAULT NULL,               -- Logro asociado al completar
    FOREIGN KEY (logro_id) REFERENCES Logros(id) ON DELETE SET NULL
);

-- Tabla de progreso de desafíos
CREATE TABLE ProgresoDesafio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    desafio_id INT NOT NULL,
    tecnicas_completadas INT DEFAULT 0,
    completado BOOLEAN DEFAULT FALSE,
    fecha_completado DATETIME DEFAULT NULL,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (desafio_id) REFERENCES Desafios(id) ON DELETE CASCADE
);