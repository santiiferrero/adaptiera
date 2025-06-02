# Adaptiera Chat Widget Vue.js

Este es un componente Vue.js que convierte tu widget HTML de chat en un componente reutilizable que se conecta a tu backend WebSocket de FastAPI.

## 🚀 Instalación Rápida

1. **Instalar dependencias:**
```bash
npm install
```

2. **Ejecutar tu servidor WebSocket:**
```bash
python main_websocket.py
```

3. **Ejecutar la aplicación Vue:**
```bash
npm run dev
```

## 📁 Estructura de Archivos

```
├── app/
│   └── components/
│       ├── ChatWidget.vue      # Componente principal del chat
│       └── ChatExample.vue     # Ejemplo de uso
├── src/
│   ├── main.js                 # Punto de entrada Vue
│   └── App.vue                 # Componente raíz
├── index.html                  # HTML principal
├── package.json                # Dependencias
└── vite.config.js             # Configuración de Vite
```

## 🎯 Uso del Componente ChatWidget

### Uso Básico

```vue
<template>
  <ChatWidget 
    @message-sent="handleMessageSent"
    @conversation-complete="handleComplete"
  />
</template>

<script>
import ChatWidget from './components/ChatWidget.vue'

export default {
  components: { ChatWidget },
  methods: {
    handleMessageSent(message) {
      console.log('Mensaje enviado:', message)
    },
    handleComplete(progress) {
      console.log('Conversación completada:', progress)
    }
  }
}
</script>
```

### Uso con Oferta de Trabajo Específica

```vue
<template>
  <ChatWidget 
    :job-offer="'job123'"
    :websocket-url="'ws://localhost:8000/chat/new_session'"
    @message-sent="handleMessageSent"
    @conversation-complete="handleComplete"
  />
</template>
```

## 🔧 Props del Componente

| Prop | Tipo | Por Defecto | Descripción |
|------|------|-------------|-------------|
| `jobOffer` | String | `null` | ID de la oferta de trabajo específica |
| `token` | String | `null` | Token de autenticación (para uso futuro) |
| `websocketUrl` | String | `'ws://localhost:8000/chat/new_session'` | URL del servidor WebSocket |

## 📡 Eventos Emitidos

| Evento | Parámetros | Descripción |
|--------|------------|-------------|
| `message-sent` | `message: string` | Se emite cuando el usuario envía un mensaje |
| `conversation-complete` | `progress: object` | Se emite cuando la conversación termina |

## 🎨 Características

### ✅ Funcionalidades Implementadas

- ✅ Conexión automática a WebSocket
- ✅ Reconexión automática en caso de pérdida de conexión
- ✅ Manejo de estados de conexión
- ✅ Scroll automático a nuevos mensajes
- ✅ Soporte para ofertas de trabajo específicas
- ✅ Eventos personalizables
- ✅ Estilos responsivos
- ✅ Indicador de estado de conexión
- ✅ Prevención de envío de mensajes vacíos
- ✅ Soporte para Enter para enviar mensajes

### 🎯 Métodos Públicos

Puedes acceder a estos métodos usando `ref`:

```vue
<template>
  <ChatWidget ref="chatWidget" />
  <button @click="clearChat">Limpiar Chat</button>
</template>

<script>
export default {
  methods: {
    clearChat() {
      this.$refs.chatWidget.clearChat()
    }
  }
}
</script>
```

| Método | Descripción |
|--------|-------------|
| `clearChat()` | Limpia todos los mensajes del chat |
| `disconnectWebSocket()` | Desconecta manualmente el WebSocket |
| `connectWebSocket()` | Reconecta manualmente el WebSocket |

## 🔄 Integración con tu Backend

El componente está diseñado para funcionar directamente con tu archivo `main_websocket.py`. Los mensajes siguen este formato:

### Mensajes del Cliente al Servidor:

```javascript
// Inicializar sesión
{
  "type": "init_session",
  "job_offer": "job123"
}

// Enviar mensaje de usuario
{
  "type": "user_message",
  "content": "Hola, estoy interesado en la posición"
}
```

### Mensajes del Servidor al Cliente:

```javascript
{
  "type": "agent_message",
  "content": "¡Hola! Bienvenido a Adaptiera...",
  "session_id": "uuid-session-id",
  "is_complete": false,
  "progress": {...}
}
```

## 🎨 Personalización de Estilos

Puedes personalizar los estilos sobrescribiendo las clases CSS:

```vue
<style>
/* Personalizar contenedor principal */
.chat-container {
  max-width: 800px !important;
  border: 2px solid #your-color !important;
}

/* Personalizar mensajes de usuario */
.message.user {
  background: #your-user-color !important;
}

/* Personalizar mensajes del agente */
.message.agent {
  background: #your-agent-color !important;
}
</style>
```

## 🔧 Scripts Disponibles

```bash
# Desarrollo
npm run dev

# Build de producción
npm run build

# Preview del build
npm run preview

# Linting
npm run lint
```

## 🌐 Despliegue

### Desarrollo
```bash
npm run dev
```
La aplicación estará disponible en `http://localhost:3000`

### Producción
```bash
npm run build
```
Los archivos de producción se generarán en la carpeta `dist/`

## 🤝 Compatibilidad

- ✅ Vue 3.x
- ✅ WebSockets nativos
- ✅ Navegadores modernos (Chrome, Firefox, Safari, Edge)
- ✅ Dispositivos móviles

## 🐛 Troubleshooting

### El WebSocket no se conecta
- Verifica que tu servidor `main_websocket.py` esté ejecutándose
- Comprueba la URL del WebSocket en los props
- Revisa la consola del navegador para errores

### Los mensajes no se envían
- Verifica que la conexión WebSocket esté activa
- Comprueba que el formato de mensajes sea correcto
- Revisa los logs del servidor

### Errores de CORS
Si tienes problemas de CORS, agrega esto a tu FastAPI:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
``` 