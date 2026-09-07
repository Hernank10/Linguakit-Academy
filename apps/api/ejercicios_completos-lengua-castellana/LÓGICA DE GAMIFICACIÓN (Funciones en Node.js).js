// ============================================================
// SISTEMA DE GAMIFICACIÓN - FUNCIONES
// ============================================================

// 2.1 Función para calcular puntos al completar una técnica
const PUNTOS_POR_TECNICA = 20;
const PUNTOS_BONUS_RACHA = 5;

async function procesarCompletarTecnica(usuarioId, tecnicaId, moduloId) {
    const connection = await pool.getConnection();
    try {
        await connection.beginTransaction();

        // 1. Verificar si ya está completada
        const [existentes] = await connection.query(
            'SELECT completado FROM ProgresoUsuario WHERE usuario_id = ? AND tecnica_id = ?',
            [usuarioId, tecnicaId]
        );
        if (existentes.length > 0 && existentes[0].completado) {
            return { mensaje: 'Ya estaba completada' };
        }

        // 2. Obtener datos del usuario
        const [usuarioData] = await connection.query(
            'SELECT puntos, nivel_actual, racha_actual, ultimo_estudio, total_tecnicas_completadas FROM PuntosUsuario WHERE usuario_id = ?',
            [usuarioId]
        );
        let puntos = usuarioData[0]?.puntos || 0;
        let racha = usuarioData[0]?.racha_actual || 0;
        let totalTecnicas = usuarioData[0]?.total_tecnicas_completadas || 0;
        const ultimoEstudio = usuarioData[0]?.ultimo_estudio;

        // 3. Calcular racha
        const ahora = new Date();
        if (ultimoEstudio) {
            const diffDias = Math.floor((ahora - new Date(ultimoEstudio)) / (1000 * 60 * 60 * 24));
            if (diffDias === 1) {
                racha++;
            } else if (diffDias > 1) {
                racha = 1; // Reinicia racha
            } else if (diffDias === 0) {
                // Mismo día, no cambia
            }
        } else {
            racha = 1;
        }

        // 4. Calcular puntos
        let puntosGanados = PUNTOS_POR_TECNICA;
        // Bonus por racha
        if (racha >= 7) puntosGanados += PUNTOS_BONUS_RACHA * 2;
        else if (racha >= 3) puntosGanados += PUNTOS_BONUS_RACHA;
        puntos += puntosGanados;
        totalTecnicas++;

        // 5. Actualizar progreso
        await connection.query(
            `INSERT INTO ProgresoUsuario (usuario_id, tecnica_id, completado, fecha_completado) 
             VALUES (?, ?, TRUE, NOW())
             ON DUPLICATE KEY UPDATE completado = TRUE, fecha_completado = NOW()`,
            [usuarioId, tecnicaId]
        );

        // 6. Actualizar puntos y racha
        await connection.query(
            `UPDATE PuntosUsuario 
             SET puntos = ?, racha_actual = ?, mejor_racha = GREATEST(mejor_racha, ?), 
                 ultimo_estudio = NOW(), total_tecnicas_completadas = ?
             WHERE usuario_id = ?`,
            [puntos, racha, racha, totalTecnicas, usuarioId]
        );

        // 7. Registrar historial
        await connection.query(
            'INSERT INTO HistorialPuntos (usuario_id, puntos, motivo, referencia_id) VALUES (?, ?, ?, ?)',
            [usuarioId, puntosGanados, 'completar_tecnica', tecnicaId]
        );

        // 8. Verificar y actualizar nivel
        const [nuevoNivel] = await connection.query(
            'SELECT nivel FROM Niveles WHERE puntos_requeridos <= ? ORDER BY puntos_requeridos DESC LIMIT 1',
            [puntos]
        );
        if (nuevoNivel.length > 0) {
            await connection.query(
                'UPDATE PuntosUsuario SET nivel_actual = ? WHERE usuario_id = ?',
                [nuevoNivel[0].nivel, usuarioId]
            );
        }

        // 9. Verificar logros
        const logrosDesbloqueados = await verificarLogros(connection, usuarioId, totalTecnicas, racha, moduloId);

        await connection.commit();

        return {
            mensaje: 'Técnica completada',
            puntosGanados,
            puntosTotales: puntos,
            racha,
            nivelActual: nuevoNivel[0]?.nivel || 1,
            logrosDesbloqueados
        };
    } catch (error) {
        await connection.rollback();
        throw error;
    } finally {
        connection.release();
    }
}

// 2.2 Función para verificar logros
async function verificarLogros(connection, usuarioId, totalTecnicas, racha, moduloId) {
    const logrosDesbloqueados = [];

    // Obtener logros ya desbloqueados
    const [desbloqueados] = await connection.query(
        'SELECT logro_id FROM LogrosUsuario WHERE usuario_id = ?',
        [usuarioId]
    );
    const idsDesbloqueados = desbloqueados.map(l => l.logro_id);

    // Obtener todos los logros
    const [logros] = await connection.query('SELECT * FROM Logros');
    
    for (const logro of logros) {
        if (idsDesbloqueados.includes(logro.id)) continue;

        let cumplido = false;
        switch (logro.criterio_tipo) {
            case 'tecnicas':
                if (parseInt(logro.criterio_valor) <= totalTecnicas) cumplido = true;
                break;
            case 'racha':
                if (parseInt(logro.criterio_valor) <= racha) cumplido = true;
                break;
            case 'dias':
                if (parseInt(logro.criterio_valor) <= racha) cumplido = true;
                break;
            case 'especial':
                // Verificar logros especiales por módulo
                if (logro.criterio_valor === 'morfema' && moduloId === 1) cumplido = true;
                if (logro.criterio_valor === 'sintaxis' && moduloId === 2) cumplido = true;
                if (logro.criterio_valor === 'ortografia' && moduloId === 3) cumplido = true;
                if (logro.criterio_valor === 'fonetica' && moduloId === 4) cumplido = true;
                if (logro.criterio_valor === 'semantica' && moduloId === 5) cumplido = true;
                break;
        }

        if (cumplido) {
            // Desbloquear logro
            await connection.query(
                'INSERT INTO LogrosUsuario (usuario_id, logro_id) VALUES (?, ?)',
                [usuarioId, logro.id]
            );
            // Sumar puntos extra
            await connection.query(
                'UPDATE PuntosUsuario SET puntos = puntos + ? WHERE usuario_id = ?',
                [logro.puntos_recompensa, usuarioId]
            );
            await connection.query(
                'INSERT INTO HistorialPuntos (usuario_id, puntos, motivo, referencia_id) VALUES (?, ?, ?, ?)',
                [usuarioId, logro.puntos_recompensa, 'logro', logro.id]
            );
            logrosDesbloqueados.push(logro);
        }
    }

    return logrosDesbloqueados;
}

// 2.3 Endpoint: Completar técnica (integra gamificación)
app.put('/api/usuario/progreso/:tecnicaId', autenticar, async (req, res) => {
    try {
        const { completado } = req.body;
        const tecnicaId = parseInt(req.params.tecnicaId);
        const usuarioId = req.usuarioId;

        if (completado) {
            // Obtener el módulo de la técnica
            const [tecnicaData] = await pool.query(
                'SELECT modulo_id FROM Tecnicas WHERE id = ?',
                [tecnicaId]
            );
            const moduloId = tecnicaData[0]?.modulo_id;

            // Procesar gamificación
            const resultado = await procesarCompletarTecnica(usuarioId, tecnicaId, moduloId);
            
            // Obtener datos actualizados
            const [puntosData] = await pool.query(
                'SELECT puntos, nivel_actual, racha_actual FROM PuntosUsuario WHERE usuario_id = ?',
                [usuarioId]
            );
            
            res.json({
                mensaje: 'Progreso actualizado',
                puntos: puntosData[0]?.puntos || 0,
                nivel: puntosData[0]?.nivel_actual || 1,
                racha: puntosData[0]?.racha_actual || 0,
                logros: resultado.logrosDesbloqueados || []
            });
        } else {
            // Desmarcar técnica (no da puntos negativos)
            await pool.query(
                'UPDATE ProgresoUsuario SET completado = FALSE, fecha_completado = NULL WHERE usuario_id = ? AND tecnica_id = ?',
                [usuarioId, tecnicaId]
            );
            res.json({ mensaje: 'Progreso actualizado' });
        }
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error al actualizar progreso' });
    }
});

// 2.4 Endpoint: Obtener gamificación del usuario
app.get('/api/usuario/gamificacion', autenticar, async (req, res) => {
    try {
        const usuarioId = req.usuarioId;

        // Datos de puntos y nivel
        const [puntosData] = await pool.query(
            `SELECT pu.*, n.titulo AS nivel_titulo, n.icono AS nivel_icono, n.descripcion AS nivel_descripcion
             FROM PuntosUsuario pu
             JOIN Niveles n ON n.nivel = pu.nivel_actual
             WHERE pu.usuario_id = ?`,
            [usuarioId]
        );

        // Logros desbloqueados
        const [logrosData] = await pool.query(
            `SELECT l.*, lu.fecha_desbloqueo
             FROM Logros l
             JOIN LogrosUsuario lu ON lu.logro_id = l.id
             WHERE lu.usuario_id = ?
             ORDER BY lu.fecha_desbloqueo DESC`,
            [usuarioId]
        );

        // Historial de puntos (últimos 10)
        const [historial] = await pool.query(
            `SELECT * FROM HistorialPuntos 
             WHERE usuario_id = ? 
             ORDER BY fecha DESC 
             LIMIT 10`,
            [usuarioId]
        );

        // Próximo nivel
        const [siguienteNivel] = await pool.query(
            `SELECT nivel, puntos_requeridos, titulo 
             FROM Niveles 
             WHERE puntos_requeridos > ? 
             ORDER BY puntos_requeridos ASC 
             LIMIT 1`,
            [puntosData[0]?.puntos || 0]
        );

        res.json({
            puntos: puntosData[0]?.puntos || 0,
            nivel: puntosData[0]?.nivel_actual || 1,
            nivel_titulo: puntosData[0]?.nivel_titulo || 'Novato',
            nivel_icono: puntosData[0]?.nivel_icono || '🌱',
            nivel_descripcion: puntosData[0]?.nivel_descripcion || '',
            racha_actual: puntosData[0]?.racha_actual || 0,
            mejor_racha: puntosData[0]?.mejor_racha || 0,
            total_tecnicas: puntosData[0]?.total_tecnicas_completadas || 0,
            siguiente_nivel: siguienteNivel[0] || null,
            logros: logrosData,
            historial: historial,
            puntos_para_siguiente: siguienteNivel[0] ? siguienteNivel[0].puntos_requeridos - (puntosData[0]?.puntos || 0) : 0
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error al obtener gamificación' });
    }
});

// 2.5 Endpoint: Ranking general
app.get('/api/ranking', autenticar, async (req, res) => {
    try {
        const [ranking] = await pool.query(`
            SELECT * FROM Vw_Ranking 
            LIMIT 50
        `);
        res.json(ranking);
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error al obtener ranking' });
    }
});

// 2.6 Endpoint: Top 10 del usuario (amigos)
app.get('/api/ranking/cercanos', autenticar, async (req, res) => {
    try {
        const usuarioId = req.usuarioId;
        const [ranking] = await pool.query(`
            SELECT * FROM Vw_Ranking 
            ORDER BY puntos DESC
        `);
        
        // Encontrar posición del usuario
        const posicion = ranking.findIndex(r => r.usuario_id === usuarioId);
        const inicio = Math.max(0, posicion - 5);
        const fin = Math.min(ranking.length, posicion + 6);
        
        res.json({
            posicion: posicion + 1,
            cercanos: ranking.slice(inicio, fin)
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error al obtener ranking cercano' });
    }
});