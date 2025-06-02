# main_websocket.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from agents.simple_agent import create_simple_rrhh_agent
import json
import uuid
from datetime import datetime
import uvicorn
import os

app = FastAPI(title="Adaptiera Chat API")

# Diccionario para sesiones activas
active_sessions = {}

def create_session(id_job_offer=None):
    session_id = str(uuid.uuid4())
    agent = create_simple_rrhh_agent(id_job_offer)
    active_sessions[session_id] = {
        "agent": agent,
        "created_at": datetime.now()
    }
    return session_id, agent

@app.websocket("/chat/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    
    # Obtener o crear agente para esta sesión
    if session_id in active_sessions:
        agent = active_sessions[session_id]["agent"]
    else:
        # Crear nueva sesión
        session_id, agent = create_session()
    
    try:
        # Mensaje inicial si no se ha iniciado
        if not agent.initialized:
            initial_message = agent.start_conversation()
            await websocket.send_text(json.dumps({
                "type": "agent_message",
                "content": initial_message,
                "session_id": session_id
            }))
        
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message["type"] == "user_message":
                # Tu agente funciona exactamente igual
                response = agent.process_user_input(message["content"])
                
                await websocket.send_text(json.dumps({
                    "type": "agent_message",
                    "content": response,
                    "is_complete": agent.is_conversation_complete(),
                    "progress": agent.get_conversation_summary()
                }))
                
            elif message["type"] == "init_session":
                # Inicializar con job_offer específico
                job_offer = message.get("job_offer")
                session_id, agent = create_session(job_offer)
                
                initial_message = agent.start_conversation()
                await websocket.send_text(json.dumps({
                    "type": "agent_message",
                    "content": initial_message,
                    "session_id": session_id
                }))
                
    except WebSocketDisconnect:
        print(f"Cliente desconectado: {session_id}")
    finally:
        # Opcional: limpiar sesión después de un tiempo
        if session_id in active_sessions:
            del active_sessions[session_id]

# Endpoint para servir el widget HTML
@app.get("/widget")
async def serve_widget():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Adaptiera Chat</title>
        <!-- Tu CSS aquí -->
    </head>
    <body>
        <div id="chat-container">
            <div id="messages"></div>
            <div id="input-container">
                <textarea id="user-input" placeholder="Escribe tu respuesta..."></textarea>
                <button id="send-btn">Enviar</button>
            </div>
        </div>
        <!-- Tu JavaScript aquí -->
    </body>
    </html>
    """

if __name__ == "__main__":
    # Railway proporciona el puerto automáticamente
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)