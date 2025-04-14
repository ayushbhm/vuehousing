// src/router/authRoutes.ts
import type { RouteRecordRaw } from 'vue-router'; 
import Auth from '../views/auth/auth.vue'; 
import CustomerRegister from '../views/auth/customer_register.vue'; 
import AuthLayout from '../layouts/AuthLayout.vue'; 
import professional_register from '../views/auth/professional_register.vue'
import admin_dashboard from '../views/admin/admin_dashboard.vue'
import professional_dashboard from '../views/professional/professional_dashboard.vue'
const authRoutes: Array<RouteRecordRaw> = [
  {
    path: '/login',
    name: 'Login',
    component: Auth,
  },
  {
    path: '/register',
    name: 'CustomerRegister',
    component: CustomerRegister, 
    meta: { layout: AuthLayout },
  },
  {
    path:'/professional_register',
    name: 'professional_register',
    component: professional_register
  },
  {
    path: '/admin_dashboard',
    name:'admin_dashboard',
    component:admin_dashboard

  },
  {
    path: '/professional_dashboard',
    name:'professional_dashboard',
    component:professional_dashboard
    }
];

export default authRoutes;