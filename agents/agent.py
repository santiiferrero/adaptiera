from langgraph.graph import StateGraph, END
from agents.nodes import decision_node

def crear_agente():
    sg = StateGraph()
    sg.add_node("decidir", decision_node)
    sg.set_entry_point("decidir")
    sg.set_finish_point(END)
    return sg.compile()
