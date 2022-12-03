import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'
import router from './router'
import './assets/styles/main.css'
import store from './store/index.js'
import CKEditor from '@ckeditor/ckeditor5-vue'

// 로그인정보 가져오기
store.dispatch('getUserInfo')

const app = createApp({
        extends: App
    })
    
app.use(CKEditor)
app.use(store)
app.use(router)

app.mount('#app')
