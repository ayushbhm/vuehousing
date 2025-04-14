import type { RouteRecordRaw } from 'vue-router'; 
import professionalsummary from '../views/professional/summary.vue';
import search from '@/views/professional/search.vue';
const professionalRoutes: Array<RouteRecordRaw> = [
    {
        path: '/professional/summary',
        component: professionalsummary
    },
    {
        path: '/professional/search',
        component: search
    }



];

export default professionalRoutes;