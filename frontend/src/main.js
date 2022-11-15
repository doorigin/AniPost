import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'
import router from './router'
import './assets/styles/main.css'
import store from './store/index.js'

const app = createApp({
        extends: App,
        beforeCreate() {
            this.$store.dispatch("getUserInfo")
        }
    })
    

app.use(store)
app.use(router)
app.mount('#app')
