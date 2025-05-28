#!/usr/bin/env python3
"""
Script para probar la carga de variables de entorno.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

def test_env_loading():
    """Prueba la carga de variables de entorno desde .env"""
    
    print("🔍 Probando carga de variables de entorno...")
    print("=" * 50)
    
    # Mostrar directorio actual
    current_dir = Path.cwd()
    print(f"📁 Directorio actual: {current_dir}")
    
    # Buscar archivos .env en diferentes ubicaciones
    possible_env_files = [
        current_dir / ".env",
        current_dir.parent / ".env",
        Path(__file__).parent / ".env",
        Path(__file__).parent.parent / ".env"
    ]
    
    print("\n🔍 Buscando archivos .env:")
    for env_file in possible_env_files:
        exists = env_file.exists()
        print(f"   {'✅' if exists else '❌'} {env_file}")
        if exists:
            print(f"      📄 Tamaño: {env_file.stat().st_size} bytes")
    
    # Cargar variables de entorno
    print("\n🔄 Cargando variables de entorno...")
    
    # Intentar cargar desde diferentes ubicaciones
    for env_file in possible_env_files:
        if env_file.exists():
            print(f"   🔄 Intentando cargar desde: {env_file}")
            load_dotenv(env_file)
            break
    else:
        print("   ⚠️ No se encontró ningún archivo .env")
        load_dotenv()  # Cargar desde ubicación por defecto
    
    # Verificar variables específicas
    print("\n📋 Variables de entorno relevantes:")
    env_vars = [
        "GROQ_API_KEY",
        "SMTP_SERVER", 
        "SMTP_PORT",
        "SENDER_EMAIL",
        "SENDER_PASSWORD",
        "RECIPIENT_EMAIL"
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            # Ocultar valores sensibles
            if "KEY" in var or "PASSWORD" in var:
                display_value = f"{value[:8]}..." if len(value) > 8 else "***"
            else:
                display_value = value
            print(f"   ✅ {var}: {display_value}")
        else:
            print(f"   ❌ {var}: No configurada")
    
    # Verificar si GROQ_API_KEY está disponible
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        print(f"\n🎉 ¡GROQ_API_KEY encontrada! (longitud: {len(groq_key)} caracteres)")
        return True
    else:
        print("\n⚠️ GROQ_API_KEY no encontrada")
        return False

if __name__ == "__main__":
    test_env_loading() 