-- Ver ranking de usuarios
SELECT * FROM Vw_Ranking LIMIT 10;

-- Ver estadísticas de un usuario específico
SELECT 
    u.nombre,
    pu.puntos,
    pu.nivel_actual,
    n.titulo AS nivel_titulo,
    pu.racha_actual,
    pu.mejor_racha,
    pu.total_tecnicas_completadas,
    (SELECT COUNT(*) FROM LogrosUsuario WHERE usuario_id = u.id) AS logros
FROM Usuarios u
JOIN PuntosUsuario pu ON pu.usuario_id = u.id
JOIN Niveles n ON n.nivel = pu.nivel_actual
WHERE u.id = 1;

-- Ver logros desbloqueados por usuario
SELECT l.*, lu.fecha_desbloqueo
FROM Logros l
JOIN LogrosUsuario lu ON lu.logro_id = l.id
WHERE lu.usuario_id = 1
ORDER BY lu.fecha_desbloqueo DESC;

-- Ver historial de puntos
SELECT * FROM HistorialPuntos 
WHERE usuario_id = 1 
ORDER BY fecha DESC 
LIMIT 20;

-- Ver progreso de técnicas por módulo
SELECT 
    m.nombre AS modulo,
    COUNT(t.id) AS total,
    SUM(CASE WHEN pu.completado = TRUE THEN 1 ELSE 0 END) AS completadas,
    ROUND((SUM(CASE WHEN pu.completado = TRUE THEN 1 ELSE 0 END) / COUNT(t.id)) * 100, 2) AS porcentaje
FROM Modulos m
JOIN Tecnicas t ON t.modulo_id = m.id
LEFT JOIN ProgresoUsuario pu ON pu.tecnica_id = t.id AND pu.usuario_id = 1
GROUP BY m.id, m.nombre;