#!/usr/bin/env python3
"""
Script de prueba para el agente conversacional de RRHH.
"""

import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path para importar módulos
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from agents.agent import crear_agente


def test_agent_conversation():
    """Prueba básica del agente conversacional"""
    
    print("🤖 Iniciando prueba del agente de RRHH...")
    print("=" * 50)
    
    # Crear el agente
    agent = crear_agente()
    
    # Iniciar conversación
    print("🚀 Iniciando conversación...")
    initial_message = agent.start_conversation()
    print(f"🤖 Agente: {initial_message}")
    print()
    
    # Simular respuestas del usuario
    test_responses = [
        "Juan Pérez García",
        "Trabajé 3 años como desarrollador Python en una startup",
        "Python, JavaScript, SQL, Docker, Git",
        "Me interesa el crecimiento profesional y los desafíos técnicos",
        "Entre 50,000 y 60,000 pesos mensuales"
    ]
    
    for i, response in enumerate(test_responses):
        print(f"👤 Usuario: {response}")
        
        # Procesar respuesta
        agent_response = agent.process_user_input(response)
        print(f"🤖 Agente: {agent_response}")
        print()
        
        # Verificar si la conversación terminó
        if agent.is_conversation_complete():
            print("✅ Conversación completada!")
            break
    
    # Mostrar resumen
    summary = agent.get_conversation_summary()
    print("📊 Resumen de la conversación:")
    print(f"   - Preguntas respondidas: {summary.get('questions_asked', 0)}")
    print(f"   - Total de preguntas: {summary.get('total_questions', 0)}")
    print(f"   - Conversación completa: {summary.get('complete', False)}")
    print(f"   - Total de mensajes: {summary.get('messages_count', 0)}")
    
    print("\n🎉 Prueba completada exitosamente!")


def test_agent_interactive():
    """Prueba interactiva del agente"""
    
    print("🤖 Modo interactivo del agente de RRHH")
    print("Escribe 'salir' para terminar")
    print("=" * 50)
    
    # Crear el agente
    agent = crear_agente()
    
    # Iniciar conversación
    initial_message = agent.start_conversation()
    print(f"🤖 Agente: {initial_message}")
    
    while True:
        try:
            # Obtener input del usuario
            user_input = input("\n👤 Tú: ").strip()
            
            if user_input.lower() in ['salir', 'exit', 'quit']:
                print("👋 ¡Hasta luego!")
                break
            
            if not user_input:
                continue
            
            # Procesar respuesta
            agent_response = agent.process_user_input(user_input)
            print(f"🤖 Agente: {agent_response}")
            
            # Verificar si la conversación terminó
            if agent.is_conversation_complete():
                print("\n✅ Conversación completada!")
                
                # Mostrar resumen
                summary = agent.get_conversation_summary()
                print("\n📊 Resumen:")
                for question, answer in summary.get('responses', {}).items():
                    print(f"   P: {question}")
                    print(f"   R: {answer}")
                    print()
                break
                
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("Selecciona el modo de prueba:")
    print("1. Prueba automática")
    print("2. Prueba interactiva")
    
    try:
        choice = input("Ingresa tu opción (1 o 2): ").strip()
        
        if choice == "1":
            test_agent_conversation()
        elif choice == "2":
            test_agent_interactive()
        else:
            print("Opción no válida. Ejecutando prueba automática...")
            test_agent_conversation()
            
    except KeyboardInterrupt:
        print("\n👋 ¡Hasta luego!")
    except Exception as e:
        print(f"❌ Error: {e}") 