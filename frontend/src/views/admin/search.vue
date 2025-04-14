<template>
    <navbar/>
    <div class="search-page">
        <h1>Admin Search Page</h1>
        <search-service-request />
    </div>
</template>
<script>
import navbar from '@/components/admin/navbar.vue';
import SearchServiceRequest from '@/components/admin/search_service_request.vue';

export default {
    name: 'AdminSearchPage',
    components: {
        navbar,
        SearchServiceRequest,
    }
}
</script>

<style scoped>
.search-page {
    padding: 20px;
}
</style>