import type { RouteRecordRaw } from 'vue-router'; 
import homepage from '../views/user/homepage.vue';
import search from '../views/user/search.vue';
import summary from '../views/user/summary.vue';
import service_detail from '../views/user/service_detail.vue';
const userRoutes: Array<RouteRecordRaw> = [
    {
        path: '/user/homepage',
        component: homepage
    },
    {
        path: '/user/search',
        component: search
    },
    {
        path: '/user/summary',
        component: summary
    },
    {
        path: '/user/service_detail/:id', // Dynamic route for service detail
        name: 'ServiceDetail', // Ensure this name matches the one used in router-link
        component: service_detail
    }
];

export default userRoutes;