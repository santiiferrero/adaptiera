<template>
  <div class="chat-container">
    <div id="messages" ref="messagesContainer" class="messages-area">
      <div 
        v-for="(message, index) in messages" 
        :key="index" 
        :class="['message', message.role]"
      >
        <strong>{{ message.role === 'user' ? '👤 Tú' : '🤖 Agente' }}:</strong> 
        {{ message.content }}
      </div>
    </div>
    
    <div class="input-container">
      <textarea 
        id="user-input" 
        v-model="userInput"
        @keydown.enter.prevent="sendMessage"
        placeholder="Escribe tu respuesta..."
        :disabled="!isConnected"
      ></textarea>
      <button 
        @click="sendMessage" 
        :disabled="!isConnected || !userInput.trim()"
        class="send-button"
      >
        {{ isConnected ? 'Enviar' : 'Conectando...' }}
      </button>
    </div>
    
    <div v-if="!isConnected" class="connection-status">
      Conectando al servidor...
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChatWidget',
  props: {
    jobOffer: {
      type: String,
      default: null
    },
    token: {
      type: String,
      default: null
    },
    websocketUrl: {
      type: String,
      default() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const host = window.location.host;
        return `${protocol}//${host}/chat/new_session`;
      }
    }
  },
  data() {
    return {
      ws: null,
      isConnected: false,
      userInput: '',
      messages: [],
      sessionId: null
    }
  },
  mounted() {
    this.connectWebSocket();
  },
  beforeUnmount() {
    this.disconnectWebSocket();
  },
  methods: {
    connectWebSocket() {
      try {
        this.ws = new WebSocket(this.websocketUrl);
        
        this.ws.onopen = () => {
          console.log('WebSocket conectado');
          this.isConnected = true;
          
          // Inicializar sesión con job offer si está disponible
          if (this.jobOffer) {
            this.ws.send(JSON.stringify({
              type: 'init_session',
              job_offer: this.jobOffer
            }));
          }
        };
        
        this.ws.onmessage = (event) => {
          const data = JSON.parse(event.data);
          
          if (data.type === 'agent_message') {
            this.addMessage('agent', data.content);
            
            // Guardar session_id si viene en la respuesta
            if (data.session_id) {
              this.sessionId = data.session_id;
            }
            
            // Emitir evento si la conversación está completa
            if (data.is_complete) {
              this.$emit('conversation-complete', data.progress);
            }
          }
        };
        
        this.ws.onclose = (event) => {
          console.log('WebSocket desconectado:', event.code, event.reason);
          this.isConnected = false;
          
          // Intentar reconectar después de 3 segundos
          if (!event.wasClean) {
            setTimeout(() => {
              console.log('Intentando reconectar...');
              this.connectWebSocket();
            }, 3000);
          }
        };
        
        this.ws.onerror = (error) => {
          console.error('Error de WebSocket:', error);
          this.isConnected = false;
        };
        
      } catch (error) {
        console.error('Error al conectar WebSocket:', error);
        this.isConnected = false;
      }
    },
    
    disconnectWebSocket() {
      if (this.ws) {
        this.ws.close();
        this.ws = null;
      }
    },
    
    sendMessage() {
      const message = this.userInput.trim();
      
      if (message && this.isConnected) {
        // Agregar mensaje del usuario
        this.addMessage('user', message);
        
        // Enviar al servidor
        this.ws.send(JSON.stringify({
          type: 'user_message',
          content: message
        }));
        
        // Limpiar input
        this.userInput = '';
        
        // Emitir evento de mensaje enviado
        this.$emit('message-sent', message);
      }
    },
    
    addMessage(role, content) {
      this.messages.push({
        role,
        content,
        timestamp: new Date()
      });
      
      // Scroll automático
      this.$nextTick(() => {
        this.scrollToBottom();
      });
    },
    
    scrollToBottom() {
      const container = this.$refs.messagesContainer;
      if (container) {
        container.scrollTop = container.scrollHeight;
      }
    },
    
    clearChat() {
      this.messages = [];
    }
  }
}
</script>

<style scoped>
.chat-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: #fff;
}

.messages-area {
  height: 400px;
  overflow-y: auto;
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  background-color: #fafafa;
}

.message {
  margin: 10px 0;
  padding: 12px;
  border-radius: 8px;
  max-width: 80%;
  word-wrap: break-word;
}

.message.user {
  background: #e3f2fd;
  margin-left: auto;
  text-align: right;
  border-bottom-right-radius: 4px;
}

.message.agent {
  background: #f1f8e9;
  margin-right: auto;
  border-bottom-left-radius: 4px;
}

.input-container {
  display: flex;
  gap: 10px;
  align-items: flex-end;
}

#user-input {
  flex: 1;
  min-height: 50px;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  resize: vertical;
  font-family: inherit;
  font-size: 14px;
}

#user-input:focus {
  outline: none;
  border-color: #2196f3;
  box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2);
}

.send-button {
  padding: 12px 20px;
  background-color: #2196f3;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s;
}

.send-button:hover:not(:disabled) {
  background-color: #1976d2;
}

.send-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.connection-status {
  text-align: center;
  padding: 10px;
  background-color: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 4px;
  margin-top: 10px;
  color: #856404;
}

/* Scrollbar personalizada */
.messages-area::-webkit-scrollbar {
  width: 6px;
}

.messages-area::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.messages-area::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.messages-area::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style> 