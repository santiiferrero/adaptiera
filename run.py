import subprocess
import os

# Obtener el directorio raíz del proyecto
root_dir = os.path.dirname(os.path.abspath(__file__))

# Configurar el entorno para el subproceso
env = os.environ.copy()
env["PYTHONPATH"] = root_dir

# Ejecutar streamlit desde el directorio raíz
subprocess.run(["streamlit", "run", "app/main.py"], env=env, cwd=root_dir)
