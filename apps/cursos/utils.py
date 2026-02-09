import subprocess
import sys

def ejecutar_codigo_python(codigo_usuario):
    try:
        # Ejecutamos el código en un proceso hijo para seguridad básica
        resultado = subprocess.run(
            [sys.executable, "-c", codigo_usuario],
            capture_output=True,
            text=True,
            timeout=2 # Evita bucles infinitos
        )
        if resultado.returncode == 0:
            return True, resultado.stdout.strip()
        else:
            return False, resultado.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "Error: El tiempo de ejecución excedió los 2 segundos."
    except Exception as e:
        return False, str(e)
