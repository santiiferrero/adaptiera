#!/usr/bin/env python3
"""
Script de prueba para verificar la interfaz de Streamlit del agente de RRHH.
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def test_imports():
    """Prueba que todas las importaciones funcionen correctamente"""
    print("🧪 Probando importaciones...")
    
    try:
        # Probar importación del agente
        from agents import crear_agente
        print("✅ Agente importado correctamente")
        
        # Probar importación de configuración
        from core.rrhh_config import (
            INTERFACE_CONFIG, 
            BUTTONS_CONFIG, 
            HELP_CONFIG, 
            CUSTOM_CSS,
            METRICS_CONFIG,
            DOWNLOAD_CONFIG
        )
        print("✅ Configuración importada correctamente")
        
        # Probar importación de la vista
        from app.views.rrhh_agent import mostrar_agente_rrhh
        print("✅ Vista del agente importada correctamente")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False


def test_agent_creation():
    """Prueba la creación del agente"""
    print("\n🧪 Probando creación del agente...")
    
    try:
        from agents import crear_agente
        
        # Crear agente
        agent = crear_agente()
        print("✅ Agente creado correctamente")
        
        # Probar métodos básicos
        summary = agent.get_conversation_summary()
        print(f"✅ Resumen inicial: {summary}")
        
        # Probar inicio de conversación
        initial_message = agent.start_conversation()
        print(f"✅ Mensaje inicial: {initial_message[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al crear agente: {e}")
        return False


def test_configuration():
    """Prueba que la configuración esté bien definida"""
    print("\n🧪 Probando configuración...")
    
    try:
        from core.rrhh_config import (
            INTERFACE_CONFIG, 
            BUTTONS_CONFIG, 
            HELP_CONFIG, 
            CUSTOM_CSS,
            METRICS_CONFIG,
            DOWNLOAD_CONFIG
        )
        
        # Verificar que las configuraciones tengan las claves esperadas
        assert "title" in INTERFACE_CONFIG
        assert "welcome_message" in INTERFACE_CONFIG
        assert "completion_message" in INTERFACE_CONFIG
        print("✅ INTERFACE_CONFIG válida")
        
        assert "start" in BUTTONS_CONFIG
        assert "restart" in BUTTONS_CONFIG
        assert "download" in BUTTONS_CONFIG
        print("✅ BUTTONS_CONFIG válida")
        
        assert "info_title" in HELP_CONFIG
        assert "expectations" in HELP_CONFIG
        assert "tips" in HELP_CONFIG
        print("✅ HELP_CONFIG válida")
        
        assert "progress_label" in METRICS_CONFIG
        assert "questions_label" in METRICS_CONFIG
        print("✅ METRICS_CONFIG válida")
        
        assert "filename" in DOWNLOAD_CONFIG
        assert "header" in DOWNLOAD_CONFIG
        print("✅ DOWNLOAD_CONFIG válida")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False


def test_data_files():
    """Prueba que los archivos de datos existan"""
    print("\n🧪 Probando archivos de datos...")
    
    try:
        # Verificar que existe el archivo de preguntas
        questions_file = Path("data/questions.json")
        if questions_file.exists():
            print("✅ Archivo de preguntas encontrado")
        else:
            print("⚠️ Archivo de preguntas no encontrado")
        
        # Verificar directorio de datos
        data_dir = Path("data")
        if data_dir.exists():
            print("✅ Directorio de datos existe")
        else:
            print("⚠️ Directorio de datos no existe")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando archivos: {e}")
        return False


def test_environment():
    """Prueba las variables de entorno"""
    print("\n🧪 Probando variables de entorno...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key:
            print("✅ GROQ_API_KEY configurada")
        else:
            print("⚠️ GROQ_API_KEY no configurada (se usará lógica simple)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando entorno: {e}")
        return False


def main():
    """Función principal de pruebas"""
    print("🚀 Iniciando pruebas de la interfaz de Streamlit")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_configuration,
        test_data_files,
        test_environment,
        test_agent_creation,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Error en prueba {test.__name__}: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Resultados: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! La interfaz está lista.")
        print("\n💡 Para ejecutar la aplicación:")
        print("   streamlit run app/main.py")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa los errores arriba.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 