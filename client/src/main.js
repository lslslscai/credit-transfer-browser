import { createApp } from 'vue'
import App from './App.vue'
import './index.css'
import router from './route/index.js'
import ElementPlus from 'element-plus'
import VueCookie from 'vue-cookies'
import '../node_modules/element-plus/dist/index.css'

const app = createApp(App)
app.config.globalProperties.$cookies = VueCookie

app.use(ElementPlus)
app.use( router )
app.mount('#app')
