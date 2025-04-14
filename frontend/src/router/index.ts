import { createRouter, createWebHistory } from 'vue-router'
import authRoutes from './authRoutes' // Import auth routes
import adminRoutes from './adminRoutes' // Import admin routes
import HomeView from '../views/HomeView.vue'
import professionalRoutes from './professionalRoutes'
import userRoutes from './userRoutes'
import Auth from '../views/auth/auth.vue'; 
const routes = [
  ...authRoutes,
  ...adminRoutes,
  ...professionalRoutes,
  ...userRoutes,
  {
    path: '/',
    name: 'home',
    component: Auth
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('../views/AboutView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
