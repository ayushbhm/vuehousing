import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import { Chart } from 'chart.js';
import Chartkick from 'vue-chartkick';

const app = createApp(App)
app.use(Chartkick.use(Chart));
app.use(createPinia())
app.use(router)

app.mount('#app')
