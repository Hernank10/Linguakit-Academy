// ============================================================
// SISTEMA DE RETROALIMENTACIÓN - FUNCIONES
// ============================================================

// 2.1 Validación de respuestas
function validarRespuesta(tipoEjercicio, respuestaEsperada, respuestaUsuario, opcionesCorrectas) {
    switch (tipoEjercicio) {
        case 'texto':
            // Validación por palabras clave
            const palabrasClave = respuestaEsperada.split(',').map(p => p.trim().toLowerCase());
            const palabrasUsuario = respuestaUsuario.toLowerCase().split(' ');
            const coincidencias = palabrasClave.filter(p => 
                palabrasUsuario.some(u => u.includes(p) || p.includes(u))
            );
            const porcentaje = (coincidencias.length / palabrasClave.length) * 100;
            return {
                esCorrecto: porcentaje >= 60,
                puntaje: Math.round(porcentaje),
                mensaje: porcentaje >= 80 ? 'Excelente respuesta' :
                         porcentaje >= 60 ? 'Buena respuesta, revisa algunos detalles' :
                         'La respuesta necesita mejorar'
            };
        
        case 'opcion_multiple':
            const correcta = opcionesCorrectas.find(o => o.id === parseInt(respuestaUsuario));
            return {
                esCorrecto: !!correcta,
                puntaje: correcta ? 100 : 0,
                mensaje: correcta ? '¡Correcto!' : 'Respuesta incorrecta. Intenta de nuevo.'
            };
        
        case 'verdadero_falso':
            const esCorrecto = respuestaUsuario.toLowerCase() === respuestaEsperada.toLowerCase();
            return {
                esCorrecto,
                puntaje: esCorrecto ? 100 : 0,
                mensaje: esCorrecto ? '¡Correcto!' : 'Incorrecto. Revisa la teoría.'
            };
        
        default:
            return { esCorrecto: false, puntaje: 0, mensaje: 'Tipo de ejercicio no soportado' };
    }
}

// 2.2 Endpoint para enviar respuesta
app.post('/api/ejercicios/:tecnicaId/validar', autenticar, async (req, res) => {
    try {
        const tecnicaId = parseInt(req.params.tecnicaId);
        const usuarioId = req.usuarioId;
        const { respuesta } = req.body;

        if (!respuesta) {
            return res.status(400).json({ error: 'Se requiere una respuesta' });
        }

        // Obtener datos de la técnica
        const [tecnica] = await pool.query(
            'SELECT tipo_ejercicio, respuesta_esperada FROM Tecnicas WHERE id = ?',
            [tecnicaId]
        );
        if (tecnica.length === 0) {
            return res.status(404).json({ error: 'Técnica no encontrada' });
        }

        // Obtener opciones si es tipo múltiple
        let opcionesCorrectas = [];
        if (tecnica[0].tipo_ejercicio === 'opcion_multiple') {
            const [opciones] = await pool.query(
                'SELECT id, opcion FROM OpcionesEjercicio WHERE tecnica_id = ? AND es_correcta = TRUE',
                [tecnicaId]
            );
            opcionesCorrectas = opciones;
        }

        // Validar respuesta
        const resultado = validarRespuesta(
            tecnica[0].tipo_ejercicio,
            tecnica[0].respuesta_esperada,
            respuesta,
            opcionesCorrectas
        );

        // Guardar intento
        await pool.query(
            `INSERT INTO IntentosEjercicio (usuario_id, tecnica_id, respuesta_usuario, es_correcto, puntaje_obtenido)
             VALUES (?, ?, ?, ?, ?)`,
            [usuarioId, tecnicaId, respuesta, resultado.esCorrecto, resultado.puntaje]
        );

        // Si es correcto, dar puntos
        let puntosGanados = 0;
        if (resultado.esCorrecto) {
            puntosGanados = 10;
            await pool.query(
                'UPDATE PuntosUsuario SET puntos = puntos + ? WHERE usuario_id = ?',
                [puntosGanados, usuarioId]
            );
            await pool.query(
                'INSERT INTO HistorialPuntos (usuario_id, puntos, motivo, referencia_id) VALUES (?, ?, ?, ?)',
                [usuarioId, puntosGanados, 'ejercicio_correcto', tecnicaId]
            );
        }

        res.json({
            ...resultado,
            puntosGanados: resultado.esCorrecto ? puntosGanados : 0,
            intentoId: result.insertId
        });

    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error al validar respuesta' });
    }
});

// 2.3 Endpoint para obtener retroalimentación específica
app.get('/api/ejercicios/:tecnicaId/retroalimentacion', autenticar, async (req, res) => {
    try {
        const tecnicaId = parseInt(req.params.tecnicaId);
        
        const [retroalimentacion] = await pool.query(
            'SELECT * FROM RetroalimentacionEjercicio WHERE tecnica_id = ?',
            [tecnicaId]
        );
        
        res.json(retroalimentacion);
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error al obtener retroalimentación' });
    }
});