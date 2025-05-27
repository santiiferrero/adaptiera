from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from agents.state import ConversationState
from agents.utils import load_questions_from_file, save_responses_to_file, simulate_email_send_simple

# Cargar variables de entorno desde .env
load_dotenv()


def initialize_conversation_node(state: ConversationState) -> ConversationState:
    """
    Nodo inicial que carga las preguntas y prepara la conversación.
    """
    print("🚀 Inicializando conversación...")
    
    # Cargar preguntas desde archivo
    questions = load_questions_from_file("data/questions.json")
    state.pending_questions = questions
    state.current_question_index = 0
    
    if questions:
        state.current_question = questions[0]
        
        # Mensaje de bienvenida
        welcome_message = AIMessage(content="""
¡Hola! Soy el asistente de RRHH de Adaptiera. 
Voy a realizarte algunas preguntas para conocerte mejor.
Responde con la mayor sinceridad posible.

Empecemos:
""")
        state.messages.append(welcome_message)
        
        # Primera pregunta
        question_message = AIMessage(content=state.current_question)
        state.messages.append(question_message)
    
    return state


def process_user_response_node(state: ConversationState) -> ConversationState:
    """
    Nodo que procesa la respuesta del usuario y decide si es satisfactoria.
    """
    print("🤔 Procesando respuesta del usuario...")
    
    # Obtener la última respuesta del usuario
    last_message = state.messages[-1] if state.messages else None
    
    if not isinstance(last_message, HumanMessage):
        print("⚠️ No se encontró respuesta del usuario")
        return state
    
    user_response = last_message.content
    current_question = state.current_question
    
    # Configurar el LLM (Groq)
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        print("⚠️ GROQ_API_KEY no configurada, usando lógica simple")
        # Lógica simple sin LLM (más permisiva)
        is_satisfactory = len(user_response.strip()) > 3
        clarification_reason = "Por favor, proporciona una respuesta más detallada" if not is_satisfactory else None
    else:
        # Usar Groq para evaluar la respuesta (modelo actualizado)
        llm = ChatGroq(api_key=groq_api_key, model="llama-3.3-70b-versatile")
        
        evaluation_prompt = f"""
        Evalúa si la siguiente respuesta es satisfactoria para la pregunta planteada:
        
        Pregunta: {current_question}
        Respuesta: {user_response}
        
        Responde SOLO con:
        - "SATISFACTORIA" si la respuesta proporciona información básica relevante a la pregunta
        - "NECESITA_CLARIFICACION: [razón]" si la respuesta está completamente vacía, es irrelevante o muy confusa
        
        Sé PERMISIVO en tu evaluación. Acepta respuestas que tengan al menos alguna relación con la pregunta, 
        incluso si son breves o no muy detalladas. Solo solicita clarificación si la respuesta realmente 
        no tiene sentido o está completamente fuera de tema.
        """
        
        try:
            evaluation = llm.invoke(evaluation_prompt).content.strip()
            
            if evaluation.startswith("SATISFACTORIA"):
                is_satisfactory = True
                clarification_reason = None
            else:
                is_satisfactory = False
                clarification_reason = evaluation.replace("NECESITA_CLARIFICACION:", "").strip()
        except Exception as e:
            print(f"Error al evaluar con Groq: {e}")
            # Fallback a lógica simple (más permisiva)
            is_satisfactory = len(user_response.strip()) > 3
            clarification_reason = "Por favor, proporciona una respuesta más detallada" if not is_satisfactory else None
    
    # Actualizar estado
    if is_satisfactory:
        # Guardar respuesta satisfactoria
        state.user_responses[current_question] = user_response
        state.needs_clarification = False
        state.clarification_reason = None
        print(f"✅ Respuesta aceptada para: {current_question}")
    else:
        state.needs_clarification = True
        state.clarification_reason = clarification_reason
        print(f"❓ Necesita clarificación: {clarification_reason}")
    
    return state


def clarification_node(state: ConversationState) -> ConversationState:
    """
    Nodo que solicita aclaración cuando la respuesta no es satisfactoria.
    """
    print("🔄 Solicitando aclaración...")
    
    clarification_message = AIMessage(content=f"""
Me gustaría que puedas ampliar tu respuesta anterior.
{state.clarification_reason}

Por favor, proporciona más detalles sobre: {state.current_question}
""")
    
    state.messages.append(clarification_message)
    return state


def next_question_node(state: ConversationState) -> ConversationState:
    """
    Nodo que avanza a la siguiente pregunta.
    """
    print("➡️ Avanzando a la siguiente pregunta...")
    
    state.current_question_index += 1
    
    if state.current_question_index < len(state.pending_questions):
        # Hay más preguntas
        state.current_question = state.pending_questions[state.current_question_index]
        
        next_question_message = AIMessage(content=f"""
Perfecto, gracias por tu respuesta.

Siguiente pregunta:
{state.current_question}
""")
        state.messages.append(next_question_message)
    else:
        # No hay más preguntas, marcar como completa
        state.conversation_complete = True
        state.current_question = None
        
        completion_message = AIMessage(content="""
¡Excelente! Hemos terminado con todas las preguntas.
Ahora voy a procesar tu información y enviar un resumen.
""")
        state.messages.append(completion_message)
    
    return state


def finalize_conversation_node(state: ConversationState) -> ConversationState:
    """
    Nodo final que guarda las respuestas y envía el correo.
    """
    print("🏁 Finalizando conversación...")
    
    # Guardar respuestas en archivo
    save_success = save_responses_to_file(state.user_responses, "data/user_responses.json")
    
    # Enviar correo (simulado por ahora)
    email_success = simulate_email_send_simple(state.user_responses)
    
    if save_success and email_success:
        final_message = AIMessage(content="""
¡Muchas gracias por tu tiempo! 

✅ Tus respuestas han sido guardadas correctamente
✅ Se ha enviado un resumen por correo electrónico

Nuestro equipo de RRHH revisará tu información y se pondrá en contacto contigo pronto.

¡Que tengas un excelente día!
""")
    else:
        final_message = AIMessage(content="""
Gracias por completar la entrevista. 
Hubo algunos problemas técnicos al procesar tu información, 
pero nuestro equipo se pondrá en contacto contigo pronto.
""")
    
    state.messages.append(final_message)
    return state


def decision_node(state: ConversationState) -> str:
    """
    Función de decisión que determina el siguiente paso en el flujo.
    Esta función NO modifica el estado, solo retorna la decisión.
    """
    print("🎯 Tomando decisión sobre el siguiente paso...")
    
    # Si la conversación está completa, ir al nodo final
    if state.conversation_complete:
        print("   → Conversación completa, finalizando...")
        return "finalize"
    
    # Si necesita aclaración, ir al nodo de aclaración
    if state.needs_clarification:
        print("   → Necesita aclaración...")
        return "clarify"
    
    # Si hay un mensaje del usuario pendiente de procesar
    if state.messages and isinstance(state.messages[-1], HumanMessage):
        print("   → Procesando respuesta del usuario...")
        return "process_response"
    
    # Si no hay pregunta actual, ir a la siguiente
    if not state.current_question:
        print("   → Avanzando a siguiente pregunta...")
        return "next_question"
    
    # Por defecto, esperar respuesta del usuario
    print("   → Esperando respuesta del usuario...")
    return "wait_for_user"


def dummy_decision_node(state: ConversationState) -> ConversationState:
    """
    Nodo dummy que no hace nada, solo para mantener la estructura del grafo.
    La lógica real está en la función decision_node que se usa para routing.
    """
    return state 