<template>
    <div>
        <UserNavbar/>
        
        <services_widget/>
        <serviceHistory/>
       
    </div>
</template>
<script>
import services_widget from '@/components/user/services_widget.vue';
import serviceHistory from '@/components/user/service_history.vue';
import customerSummary from '@/components/user/summary.vue';
import UserNavbar from '@/components/user/navbar.vue';
export default {
    name: 'userHomepage',
    components: {
        services_widget,
        serviceHistory,
        customerSummary,
        UserNavbar
    }
}
</script>
