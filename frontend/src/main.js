import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'

import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import './assets/css/style.css'

// Font Awesome
const faLink = document.createElement('link')
faLink.rel = 'stylesheet'
faLink.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css'
document.head.appendChild(faLink)

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

app.mount('#app')