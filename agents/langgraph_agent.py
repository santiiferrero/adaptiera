from typing import Dict, Any, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langgraph.graph.message import add_messages

from agents.state import ConversationState
from agents.nodes import (
    initialize_conversation_node,
    process_user_response_node,
    clarification_node,
    next_question_node,
    finalize_conversation_node,
    decision_node,
    dummy_decision_node
)


class GraphState(TypedDict):
    """Estado compatible con LangGraph"""
    messages: Annotated[list[BaseMessage], add_messages]
    pending_questions: list[str]
    user_responses: dict[str, str]
    current_question: str
    current_question_index: int
    needs_clarification: bool
    clarification_reason: str
    conversation_complete: bool
    metadata: dict[str, Any]


def graph_to_conversation_state(graph_state: GraphState) -> ConversationState:
    """Convierte GraphState a ConversationState"""
    state = ConversationState()
    state.messages = graph_state.get("messages", [])
    state.pending_questions = graph_state.get("pending_questions", [])
    state.user_responses = graph_state.get("user_responses", {})
    state.current_question = graph_state.get("current_question")
    state.current_question_index = graph_state.get("current_question_index", 0)
    state.needs_clarification = graph_state.get("needs_clarification", False)
    state.clarification_reason = graph_state.get("clarification_reason")
    state.conversation_complete = graph_state.get("conversation_complete", False)
    state.metadata = graph_state.get("metadata", {})
    return state


def conversation_to_graph_state(conv_state: ConversationState) -> GraphState:
    """Convierte ConversationState a GraphState"""
    return GraphState(
        messages=conv_state.messages,
        pending_questions=conv_state.pending_questions,
        user_responses=conv_state.user_responses,
        current_question=conv_state.current_question or "",
        current_question_index=conv_state.current_question_index,
        needs_clarification=conv_state.needs_clarification,
        clarification_reason=conv_state.clarification_reason or "",
        conversation_complete=conv_state.conversation_complete,
        metadata=conv_state.metadata
    )


# Funciones wrapper para los nodos
def wrap_initialize_node(state: GraphState) -> GraphState:
    conv_state = graph_to_conversation_state(state)
    result = initialize_conversation_node(conv_state)
    return conversation_to_graph_state(result)


def wrap_process_response_node(state: GraphState) -> GraphState:
    conv_state = graph_to_conversation_state(state)
    result = process_user_response_node(conv_state)
    return conversation_to_graph_state(result)


def wrap_clarification_node(state: GraphState) -> GraphState:
    conv_state = graph_to_conversation_state(state)
    result = clarification_node(conv_state)
    return conversation_to_graph_state(result)


def wrap_next_question_node(state: GraphState) -> GraphState:
    conv_state = graph_to_conversation_state(state)
    result = next_question_node(conv_state)
    return conversation_to_graph_state(result)


def wrap_finalize_node(state: GraphState) -> GraphState:
    conv_state = graph_to_conversation_state(state)
    result = finalize_conversation_node(conv_state)
    return conversation_to_graph_state(result)


def wrap_decision_routing(state: GraphState) -> str:
    conv_state = graph_to_conversation_state(state)
    return decision_node(conv_state)


def wrap_dummy_decision_node(state: GraphState) -> GraphState:
    return state


class AdaptieraRRHHAgent:
    """
    Agente conversacional de RRHH usando LangGraph.
    
    Este agente maneja entrevistas automatizadas, recopila respuestas,
    decide cuándo repreguntar y envía resúmenes por correo.
    """
    
    def __init__(self):
        self.graph = self._create_graph()
        self.current_state = None
    
    def _create_graph(self) -> StateGraph:
        """Crea el grafo de estados de LangGraph"""
        
        # Crear el grafo con el estado compatible con LangGraph
        workflow = StateGraph(GraphState)
        
        # Agregar nodos usando las funciones wrapper
        workflow.add_node("initialize", wrap_initialize_node)
        workflow.add_node("process_response", wrap_process_response_node)
        workflow.add_node("clarify", wrap_clarification_node)
        workflow.add_node("next_question", wrap_next_question_node)
        workflow.add_node("finalize", wrap_finalize_node)
        workflow.add_node("decision", wrap_dummy_decision_node)
        
        # Definir el punto de entrada
        workflow.set_entry_point("initialize")
        
        # Agregar aristas condicionales desde el nodo de decisión
        workflow.add_conditional_edges(
            "decision",
            wrap_decision_routing,
            {
                "process_response": "process_response",
                "clarify": "clarify", 
                "next_question": "next_question",
                "finalize": "finalize",
                "wait_for_user": END
            }
        )
        
        # Aristas desde otros nodos hacia decisión
        workflow.add_edge("initialize", "decision")
        workflow.add_edge("process_response", "decision")
        workflow.add_edge("clarify", "decision")
        workflow.add_edge("next_question", "decision")
        workflow.add_edge("finalize", END)
        
        return workflow.compile()
    
    def start_conversation(self) -> str:
        """
        Inicia una nueva conversación.
        
        Returns:
            Mensaje inicial del agente
        """
        # Crear nuevo estado inicial
        initial_state = GraphState(
            messages=[],
            pending_questions=[],
            user_responses={},
            current_question="",
            current_question_index=0,
            needs_clarification=False,
            clarification_reason="",
            conversation_complete=False,
            metadata={}
        )
        
        # Ejecutar el grafo hasta que necesite input del usuario
        result = self.graph.invoke(initial_state)
        self.current_state = result
        
        # Retornar el último mensaje del agente
        if self.current_state.get("messages"):
            last_messages = [msg for msg in self.current_state["messages"] if isinstance(msg, AIMessage)]
            if last_messages:
                return last_messages[-1].content
        
        return "¡Hola! Soy el asistente de RRHH. ¿Cómo puedo ayudarte?"
    
    def process_user_input(self, user_input: str) -> str:
        """
        Procesa la entrada del usuario y retorna la respuesta del agente.
        
        Args:
            user_input: Mensaje del usuario
            
        Returns:
            Respuesta del agente
        """
        if not self.current_state:
            return self.start_conversation()
        
        # Agregar mensaje del usuario al estado
        user_message = HumanMessage(content=user_input)
        current_messages = list(self.current_state.get("messages", []))
        current_messages.append(user_message)
        
        # Actualizar el estado con el nuevo mensaje
        updated_state = dict(self.current_state)
        updated_state["messages"] = current_messages
        
        # Ejecutar el grafo
        result = self.graph.invoke(updated_state)
        self.current_state = result
        
        # Retornar el último mensaje del agente
        if self.current_state.get("messages"):
            messages = self.current_state["messages"]
            # Buscar el último mensaje del agente después del mensaje del usuario
            ai_messages = []
            for i, msg in enumerate(messages):
                if isinstance(msg, AIMessage) and i > 0:
                    # Verificar que hay un mensaje del usuario antes
                    prev_msg = messages[i-1]
                    if isinstance(prev_msg, HumanMessage) and prev_msg.content == user_input:
                        ai_messages.append(msg)
            
            if ai_messages:
                return ai_messages[-1].content
            
            # Fallback: último mensaje de IA
            last_ai_messages = [msg for msg in messages if isinstance(msg, AIMessage)]
            if last_ai_messages:
                return last_ai_messages[-1].content
        
        return "Lo siento, hubo un problema procesando tu respuesta. ¿Puedes intentar de nuevo?"
    
    def is_conversation_complete(self) -> bool:
        """
        Verifica si la conversación ha terminado.
        
        Returns:
            True si la conversación está completa
        """
        return self.current_state and self.current_state.get("conversation_complete", False)
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """
        Obtiene un resumen de la conversación.
        
        Returns:
            Diccionario con el resumen de la conversación
        """
        if not self.current_state:
            return {}
        
        return {
            "responses": self.current_state.get("user_responses", {}),
            "questions_asked": len(self.current_state.get("user_responses", {})),
            "total_questions": len(self.current_state.get("pending_questions", [])),
            "complete": self.current_state.get("conversation_complete", False),
            "messages_count": len(self.current_state.get("messages", []))
        }
    
    def reset_conversation(self):
        """Reinicia la conversación"""
        self.current_state = None


# Función de conveniencia para crear una instancia del agente
def create_rrhh_agent() -> AdaptieraRRHHAgent:
    """
    Crea una nueva instancia del agente de RRHH.
    
    Returns:
        Instancia del agente configurada
    """
    return AdaptieraRRHHAgent() 