// ============================================================
// SISTEMA DE DESAFÍOS - FUNCIONES
// ============================================================

async function verificarDesafios(connection, usuarioId) {
    const hoy = new Date().toISOString().split('T')[0];
    
    // Obtener desafíos activos
    const [desafios] = await connection.query(
        `SELECT * FROM Desafios 
         WHERE ? BETWEEN fecha_inicio AND fecha_fin`,
        [hoy]
    );
    
    const resultados = [];
    for (const desafio of desafios) {
        // Verificar progreso del usuario
        let [progreso] = await connection.query(
            `SELECT * FROM ProgresoDesafio 
             WHERE usuario_id = ? AND desafio_id = ?`,
            [usuarioId, desafio.id]
        );
        
        if (progreso.length === 0) {
            // Crear registro de progreso
            const [result] = await connection.query(
                `INSERT INTO ProgresoDesafio (usuario_id, desafio_id, tecnicas_completadas)
                 VALUES (?, ?, 0)`,
                [usuarioId, desafio.id]
            );
            progreso = [{ id: result.insertId, tecnicas_completadas: 0, completado: false }];
        }
        
        // Contar técnicas completadas en el período del desafío
        const [tecnicas] = await connection.query(
            `SELECT COUNT(*) as total FROM ProgresoUsuario 
             WHERE usuario_id = ? AND completado = TRUE 
             AND fecha_completado BETWEEN ? AND ?`,
            [usuarioId, desafio.fecha_inicio, desafio.fecha_fin]
        );
        
        const completadas = tecnicas[0]?.total || 0;
        
        // Actualizar progreso
        await connection.query(
            `UPDATE ProgresoDesafio 
             SET tecnicas_completadas = ? 
             WHERE usuario_id = ? AND desafio_id = ?`,
            [completadas, usuarioId, desafio.id]
        );
        
        // Verificar si completó el desafío
        if (!progreso[0].completado && completadas >= desafio.objetivo) {
            await connection.query(
                `UPDATE ProgresoDesafio 
                 SET completado = TRUE, fecha_completado = NOW() 
                 WHERE usuario_id = ? AND desafio_id = ?`,
                [usuarioId, desafio.id]
            );
            
            // Dar puntos extra
            await connection.query(
                `UPDATE PuntosUsuario 
                 SET puntos = puntos + ? 
                 WHERE usuario_id = ?`,
                [desafio.puntos_recompensa, usuarioId]
            );
            
            await connection.query(
                `INSERT INTO HistorialPuntos (usuario_id, puntos, motivo, referencia_id)
                 VALUES (?, ?, 'desafio_completado', ?)`,
                [usuarioId, desafio.puntos_recompensa, desafio.id]
            );
            
            // Desbloquear logro asociado si existe
            if (desafio.logro_id) {
                await connection.query(
                    `INSERT IGNORE INTO LogrosUsuario (usuario_id, logro_id)
                     VALUES (?, ?)`,
                    [usuarioId, desafio.logro_id]
                );
            }
            
            resultados.push({ desafio: desafio.titulo, completado: true });
        }
    }
    
    return resultados;
}

// Endpoint para obtener desafíos activos
app.get('/api/desafios/activos', autenticar, async (req, res) => {
    try {
        const hoy = new Date().toISOString().split('T')[0];
        const [desafios] = await pool.query(
            `SELECT d.*, pd.tecnicas_completadas, pd.completado
             FROM Desafios d
             LEFT JOIN ProgresoDesafio pd ON pd.desafio_id = d.id AND pd.usuario_id = ?
             WHERE ? BETWEEN d.fecha_inicio AND d.fecha_fin`,
            [req.usuarioId, hoy]
        );
        res.json(desafios);
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error al obtener desafíos' });
    }
});