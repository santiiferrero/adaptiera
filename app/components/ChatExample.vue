<template>
  <div class="app-container">
    <h1>Adaptiera - Chat de RRHH</h1>
    
    <!-- Ejemplo básico -->
    <div class="section">
      <h2>Chat Básico</h2>
      <ChatWidget 
        @message-sent="onMessageSent"
        @conversation-complete="onConversationComplete"
      />
    </div>
    
    <!-- Ejemplo con job offer -->
    <div class="section">
      <h2>Chat con Oferta de Trabajo Específica</h2>
      <div class="controls">
        <input 
          v-model="selectedJobOffer" 
          placeholder="ID de oferta de trabajo"
          class="job-input"
        />
        <button @click="startJobSpecificChat" class="start-btn">
          Iniciar Chat
        </button>
      </div>
      
      <ChatWidget 
        v-if="showJobChat"
        :job-offer="selectedJobOffer"
        :websocket-url="websocketUrl"
        @message-sent="onMessageSent"
        @conversation-complete="onConversationComplete"
        ref="jobChatWidget"
      />
    </div>
    
    <!-- Estado de la conversación -->
    <div v-if="conversationProgress" class="progress-section">
      <h3>Progreso de la Conversación</h3>
      <pre>{{ JSON.stringify(conversationProgress, null, 2) }}</pre>
    </div>
  </div>
</template>

<script>
import ChatWidget from './ChatWidget.vue'

export default {
  name: 'ChatExample',
  components: {
    ChatWidget
  },
  data() {
    return {
      selectedJobOffer: '',
      showJobChat: false,
      conversationProgress: null,
      websocketUrl: 'ws://localhost:8000/chat/new_session'
    }
  },
  methods: {
    onMessageSent(message) {
      console.log('Mensaje enviado:', message);
      // Aquí puedes agregar lógica adicional cuando se envía un mensaje
    },
    
    onConversationComplete(progress) {
      console.log('Conversación completada:', progress);
      this.conversationProgress = progress;
      
      // Aquí puedes manejar el final de la conversación
      // Por ejemplo, mostrar un resumen o redireccionar
    },
    
    startJobSpecificChat() {
      if (this.selectedJobOffer.trim()) {
        this.showJobChat = false; // Reset
        this.$nextTick(() => {
          this.showJobChat = true;
        });
      }
    },
    
    clearJobChat() {
      if (this.$refs.jobChatWidget) {
        this.$refs.jobChatWidget.clearChat();
      }
    }
  }
}
</script>

<style scoped>
.app-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
}

.section {
  margin: 40px 0;
  padding: 20px;
  border: 1px solid #eee;
  border-radius: 10px;
  background-color: #fafafa;
}

h2 {
  color: #555;
  margin-bottom: 20px;
}

.controls {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  align-items: center;
}

.job-input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
}

.start-btn {
  padding: 10px 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
}

.start-btn:hover {
  background-color: #45a049;
}

.progress-section {
  margin-top: 30px;
  padding: 20px;
  background-color: #f0f8ff;
  border-radius: 10px;
  border: 1px solid #b3d9ff;
}

.progress-section h3 {
  color: #1976d2;
  margin-bottom: 15px;
}

pre {
  background-color: #fff;
  padding: 15px;
  border-radius: 5px;
  border: 1px solid #ddd;
  overflow-x: auto;
  font-size: 12px;
}
</style> 