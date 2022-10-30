import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'
import router from './router'
import './assets/styles/main.css'

const app = createApp(App)
app.use(router)
app.mount('#app')
