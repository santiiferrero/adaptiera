<template>
  <div id="app">
    <ChatExample />
  </div>
</template>

<script>
import ChatExample from '../app/components/ChatExample.vue'

export default {
  name: 'App',
  components: {
    ChatExample
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
}

#app {
  min-height: 100vh;
  padding: 20px 0;
}
</style> 