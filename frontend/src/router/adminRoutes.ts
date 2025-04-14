import type { RouteRecordRaw } from 'vue-router'; 
import adminsummary from '../views/admin/summary.vue';
import search from '@/views/admin/search.vue';
const adminRoutes: Array<RouteRecordRaw> = [
    {
        path: '/admin/summary',
        component: adminsummary
    },
    {
        path: '/admin/search',
        component: search

    }



];

export default adminRoutes;