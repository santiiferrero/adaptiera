#!/usr/bin/env python3
"""
Script de inicio para la aplicación de Streamlit del agente de RRHH.
Este script maneja las importaciones y configuraciones necesarias.
"""

import sys
import os
from pathlib import Path
import subprocess

def setup_environment():
    """Configurar el entorno para la aplicación"""
    # Agregar el directorio actual al path
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))
    
    # Verificar que existe el archivo .env
    env_file = current_dir / ".env"
    if not env_file.exists():
        print("⚠️ Archivo .env no encontrado. Creando uno básico...")
        with open(env_file, "w") as f:
            f.write("# Configuración del agente de RRHH\n")
            f.write("GROQ_API_KEY=tu_clave_aqui\n")
        print("✅ Archivo .env creado. Por favor configura tu GROQ_API_KEY.")
    
    # Verificar que existen los directorios necesarios
    directories = ["app", "app/views", "app/config", "agents", "data", "tools"]
    for directory in directories:
        dir_path = current_dir / directory
        if not dir_path.exists():
            print(f"⚠️ Directorio {directory} no encontrado. Creándolo...")
            dir_path.mkdir(parents=True, exist_ok=True)
    
    print("✅ Entorno configurado correctamente.")

def check_dependencies():
    """Verificar que las dependencias estén instaladas"""
    required_packages = [
        "streamlit",
        "langchain-groq", 
        "python-dotenv",
        "pydantic"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Faltan las siguientes dependencias:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Instálalas con:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ Todas las dependencias están instaladas.")
    return True

def run_streamlit():
    """Ejecutar la aplicación de Streamlit"""
    app_file = Path(__file__).parent / "app" / "main.py"
    
    if not app_file.exists():
        print("❌ No se encontró el archivo app/main.py")
        return False
    
    print("🚀 Iniciando aplicación de Streamlit...")
    print("📱 La aplicación se abrirá en tu navegador automáticamente.")
    print("🔗 URL: http://localhost:8501")
    print("\n💡 Para detener la aplicación, presiona Ctrl+C")
    
    try:
        # Ejecutar Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(app_file),
            "--server.headless", "false",
            "--server.port", "8501"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al ejecutar Streamlit: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 Aplicación detenida por el usuario.")
        return True
    
    return True

def main():
    """Función principal"""
    print("🤖 Agente de RRHH - Adaptiera")
    print("=" * 40)
    
    # Configurar entorno
    setup_environment()
    
    # Verificar dependencias
    if not check_dependencies():
        print("\n❌ No se puede continuar sin las dependencias necesarias.")
        sys.exit(1)
    
    # Ejecutar aplicación
    success = run_streamlit()
    
    if success:
        print("\n✅ Aplicación ejecutada exitosamente.")
    else:
        print("\n❌ Hubo un error al ejecutar la aplicación.")
        sys.exit(1)

if __name__ == "__main__":
    main() 